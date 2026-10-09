/* ==========================================
   Data vocabularies
========================================== */

const windDirectionNames = {
  N: "北", NNE: "北北東", NE: "北東", ENE: "東北東",
  E: "東", ESE: "東南東", SE: "南東", SSE: "南南東",
  S: "南", SSW: "南南西", SW: "南西", WSW: "西南西",
  W: "西", WNW: "西北西", NW: "北西", NNW: "北北西", CALM: "静穏",
};

const weatherNames = {
  0: "快晴", 1: "晴れ", 2: "薄曇り", 3: "曇り",
  10: "煙霧", 40: "霧", 50: "霧雨", 60: "雨",
  70: "にわか雨", 80: "雪", 85: "にわか雪", 88: "みぞれ", 90: "不明",
};

const chartElements = {
  temperature_c: { label: "気温", unit: "℃" },
  relative_humidity_percent: { label: "相対湿度", unit: "%" },
  wind_speed_m_s: { label: "風速", unit: "m/s" },
  station_pressure_hpa: { label: "現地気圧", unit: "hPa" },
  precipitation_mm: { label: "降水量", unit: "mm" },
};

const elementNames = {
  global_solar_radiation_mj_m2: "全天日射量",
  dew_point_temperature_c: "露点温度",
};


/* ==========================================
   Application state
========================================== */

const state = {
  availableDatasets: [],
  selectedDataset: null,
  datasetMetadata: {},
  observations: [],
  observationsByDateAndHour: new Map(),
  dailySummariesByDate: new Map(),
  availableDates: [],
  selectedDate: null,
  selectedHour: 12,
  selectedChartElement: "temperature_c",
};

const elements = {
  datasetSelect: document.querySelector("#dataset-select"),
  dateSelect: document.querySelector("#date-select"),
  hourRange: document.querySelector("#hour-range"),
  hourOutput: document.querySelector("#hour-output"),
  selectedMoment: document.querySelector("#selected-moment"),
  loadingMessage: document.querySelector("#loading-message"),
  errorMessage: document.querySelector("#error-message"),
  observationGrid: document.querySelector("#observation-grid"),
  chartElementSelect: document.querySelector("#chart-element-select"),
  dailyChart: document.querySelector("#daily-chart"),
  chartTitle: document.querySelector("#chart-title"),
  chartDescription: document.querySelector("#chart-description"),
  chartEmptyMessage: document.querySelector("#chart-empty-message"),
  canonicalDataLink: document.querySelector("#canonical-data-link"),
  validationReportLink: document.querySelector("#validation-report-link"),
  availabilityMessage: document.querySelector("#availability-message"),
  availabilityMessageText: document.querySelector("#availability-message-text"),
  weatherLabel: document.querySelector("#weather-label"),
};


/* ==========================================
   Data loading
========================================== */

async function initializeApplication() {
  try {
    const response = await fetch("data/index.json");
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }

    state.availableDatasets = await response.json();
    if (!state.availableDatasets.length) {
      throw new Error("No datasets are available");
    }

    elements.datasetSelect.replaceChildren();
    for (const dataset of state.availableDatasets) {
      const option = document.createElement("option");
      option.value = `${dataset.year}-${String(dataset.month).padStart(2, "0")}`;
      option.textContent = dataset.label;
      elements.datasetSelect.append(option);
    }

    state.selectedDataset = state.availableDatasets.at(-1);
    elements.datasetSelect.value = datasetKey(state.selectedDataset);
    elements.datasetSelect.disabled = false;
    elements.datasetSelect.addEventListener("change", async (event) => {
      state.selectedDataset = state.availableDatasets.find(
        (dataset) => datasetKey(dataset) === event.target.value,
      );
      await loadSelectedDataset();
    });

    initializeControls();
    await loadSelectedDataset();
  } catch (error) {
    showLoadError(error);
  }
}

async function loadSelectedDataset() {
  elements.loadingMessage.hidden = false;
  elements.errorMessage.hidden = true;
  elements.observationGrid.hidden = true;

  try {
    const response = await fetch(`data/${state.selectedDataset.data_path}`);
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }

    const documentData = await response.json();
    state.datasetMetadata = documentData.dataset;
    state.observations = documentData.observations;
    state.availableDates = [...new Set(state.observations.map((item) => item.source_date))];
    state.selectedDate = state.availableDates[0];
    state.observationsByDateAndHour.clear();
    state.dailySummariesByDate.clear();

    for (const observation of state.observations) {
      state.observationsByDateAndHour.set(
        `${observation.source_date}#${observation.source_hour}`,
        observation,
      );
    }
    for (const summary of documentData.daily_summaries ?? []) {
      state.dailySummariesByDate.set(summary.date, summary);
    }

    const weatherHours = state.datasetMetadata.observation_schedules?.weather_code ?? [12];
    state.selectedHour = weatherHours[0];
    elements.hourRange.value = state.selectedHour;

    populateDateOptions();
    updateProvenanceLinks();
    renderAvailabilityMessage();
    elements.loadingMessage.hidden = true;
    elements.observationGrid.hidden = false;
    renderSelectedObservation();
  } catch (error) {
    showLoadError(error);
  }
}

function datasetKey(dataset) {
  return `${dataset.year}-${String(dataset.month).padStart(2, "0")}`;
}

function showLoadError(error) {
  elements.loadingMessage.hidden = true;
  elements.errorMessage.hidden = false;
  elements.errorMessage.textContent = "観測データを読み込めませんでした。時間をおいて再度お試しください。";
  console.error(error);
}


/* ==========================================
   Controls
========================================== */

function initializeControls() {
  elements.dateSelect.disabled = false;
  elements.hourRange.disabled = false;
  elements.chartElementSelect.disabled = false;

  elements.dateSelect.addEventListener("change", (event) => {
    state.selectedDate = event.target.value;
    renderSelectedObservation();
  });

  elements.hourRange.addEventListener("input", (event) => {
    state.selectedHour = Number(event.target.value);
    renderSelectedObservation();
  });

  elements.chartElementSelect.addEventListener("change", (event) => {
    state.selectedChartElement = event.target.value;
    renderDailyChart();
  });
}

function populateDateOptions() {
  elements.dateSelect.replaceChildren();
  for (const sourceDate of state.availableDates) {
    const option = document.createElement("option");
    option.value = sourceDate;
    option.textContent = formatJapaneseDate(sourceDate);
    elements.dateSelect.append(option);
  }
  elements.dateSelect.value = state.selectedDate;
}

function updateProvenanceLinks() {
  const repositoryBaseUrl = "https://github.com/kojikomatsuzaki/hitachi-weather-data/blob/main/";
  elements.canonicalDataLink.href = repositoryBaseUrl + state.selectedDataset.yaml_path;
  elements.validationReportLink.href = repositoryBaseUrl + state.selectedDataset.report_path;
}


/* ==========================================
   Observation rendering
========================================== */

function renderSelectedObservation() {
  const observation = state.observationsByDateAndHour.get(
    `${state.selectedDate}#${state.selectedHour}`,
  ) ?? { values: {}, flags: {} };

  elements.hourOutput.textContent = `${state.selectedHour}時`;
  elements.selectedMoment.textContent = `${formatJapaneseDate(state.selectedDate)} ${state.selectedHour}時`;

  const displayValues = {
    ...observation.values,
    wind_direction: formatWindDirection(observation.values.wind_direction),
    weather_code: formatWeather(observation.values.weather_code),
  };
  const precipitationLayout = state.datasetMetadata.source_table_layouts?.precipitation_mm;
  if (precipitationLayout?.available_as === "daily_summary") {
    displayValues.precipitation_mm =
      state.dailySummariesByDate.get(state.selectedDate)?.precipitation?.total_mm;
  }

  for (const target of document.querySelectorAll("[data-value]")) {
    const elementId = target.dataset.value;
    const unavailable = isUnavailableForPeriod(elementId);
    const flag = observation.flags?.[elementId];
    const rawValue = observation.raw_values?.[elementId];
    target.textContent = unavailable
      ? "原データに項目なし"
      : formatSourceValue(displayValues[elementId], flag, rawValue);
    const unit = target.parentElement?.querySelector(".unit");
    if (unit) unit.hidden = unavailable || displayValues[elementId] === null
      || displayValues[elementId] === undefined;
  }

  const precipitationNote = document.querySelector('[data-note="precipitation_mm"]');
  precipitationNote.textContent = precipitationLayout?.available_as === "daily_summary"
    ? "時刻別値はなく、この日の日合計を表示"
    : formatSourceFlag(observation.flags?.precipitation_mm);

  const weatherNote = document.querySelector('[data-note="weather_code"]');
  const weatherHour = state.datasetMetadata.observation_schedules?.weather_code?.[0];
  elements.weatherLabel.textContent = weatherHour ? `${weatherHour}時の天気` : "天気";
  weatherNote.textContent = state.selectedHour === weatherHour
    ? "原資料の天気表記から表示"
    : weatherHour ? `${weatherHour}時のみ記録` : "記録時刻を確認できません";

  renderDailyChart();
}

function formatValue(value) {
  if (value === null || value === undefined) return "—";
  return String(value);
}

function formatSourceValue(value, flag, rawValue) {
  if (flag === "unrecognized_source_value") {
    return `「${String(rawValue)}」と原データに表記`;
  }
  if (flag === "source_blank" || flag === "source_whitespace") {
    return "原データで無表記";
  }
  return formatValue(value);
}

function formatWindDirection(code) {
  if (code === null || code === undefined) return null;
  const name = windDirectionNames[code] ?? code;
  return `${name}（${code}）`;
}

function formatWeather(code) {
  if (code === null || code === undefined) return null;
  return weatherNames[code] ?? `コード ${code}`;
}

function isUnavailableForPeriod(elementId) {
  return state.datasetMetadata.element_availability?.[elementId]?.status
    === "not_available_for_period";
}

function renderAvailabilityMessage() {
  const unavailableElements = Object.entries(
    state.datasetMetadata.element_availability ?? {},
  ).filter(([, details]) => details.status === "not_available_for_period");

  const sourceTableMessages = [];
  const sourceTableLayouts = state.datasetMetadata.source_table_layouts ?? {};
  if (sourceTableLayouts.precipitation_mm?.status === "no_hourly_values_in_month") {
    sourceTableMessages.push("降水量は時刻別欄が空白のため、日合計を表示します");
  }
  if (sourceTableLayouts.sea_level_pressure_hpa?.status === "no_values_in_month") {
    sourceTableMessages.push("海面気圧は表がありますが、この月の値はありません");
  }

  if (!unavailableElements.length && !sourceTableMessages.length) {
    elements.availabilityMessage.hidden = true;
    elements.availabilityMessageText.textContent = "";
    return;
  }

  const names = unavailableElements.map(([elementId]) => elementNames[elementId] ?? elementId);
  const messages = [];
  if (names.length) {
    messages.push(
      `${names.join("・")}は、この年の公開資料に収録されていません。欠測値とは区別しています`,
    );
  }
  messages.push(...sourceTableMessages);
  elements.availabilityMessageText.textContent = `${messages.join("。")}。`;
  elements.availabilityMessage.hidden = false;
}

function formatSourceFlag(flag) {
  const flagLabels = {
    source_blank: "原データで無表記",
    source_whitespace: "原データで無表記",
    source_dash: "原資料では「-」",
    source_triple_asterisk: "原資料では「***」",
    unrecognized_source_value: "原データの未解釈表記",
  };
  return flagLabels[flag] ?? "";
}

function formatJapaneseDate(sourceDate) {
  const [year, month, day] = sourceDate.split("-").map(Number);
  const date = new Date(year, month - 1, day);
  const weekday = new Intl.DateTimeFormat("ja-JP", { weekday: "short" }).format(date);
  return `${year}年${month}月${day}日（${weekday}）`;
}


/* ==========================================
   Daily SVG chart
========================================== */

function renderDailyChart() {
  const elementDefinition = chartElements[state.selectedChartElement];
  const dailyObservations = state.observations.filter(
    (item) => item.source_date === state.selectedDate,
  );
  const points = dailyObservations
    .map((item) => ({
      hour: item.source_hour,
      value: item.values[state.selectedChartElement],
    }))
    .filter((point) => Number.isFinite(point.value));

  elements.dailyChart.querySelectorAll("g").forEach((group) => group.remove());
  elements.chartTitle.textContent = `${formatJapaneseDate(state.selectedDate)}の${elementDefinition.label}`;
  elements.chartDescription.textContent = `原資料に記録された時刻の${elementDefinition.label}を${elementDefinition.unit}で示します。`;

  if (points.length === 0) {
    elements.chartEmptyMessage.hidden = false;
    return;
  }
  elements.chartEmptyMessage.hidden = true;

  const width = 760;
  const height = 300;
  const margin = { top: 28, right: 28, bottom: 46, left: 68 };
  const plotWidth = width - margin.left - margin.right;
  const plotHeight = height - margin.top - margin.bottom;
  const values = points.map((point) => point.value);
  let minimum = Math.min(...values);
  let maximum = Math.max(...values);
  const rawRange = maximum - minimum;
  const padding = rawRange === 0 ? Math.max(Math.abs(maximum) * 0.1, 1) : rawRange * 0.12;
  minimum -= padding;
  maximum += padding;

  const x = (hour) => margin.left + ((hour - 1) / 23) * plotWidth;
  const y = (value) => margin.top + ((maximum - value) / (maximum - minimum)) * plotHeight;
  const chartGroup = createSvgElement("g");

  for (let index = 0; index <= 4; index += 1) {
    const gridY = margin.top + (index / 4) * plotHeight;
    const gridValue = maximum - (index / 4) * (maximum - minimum);
    chartGroup.append(createSvgElement("line", {
      x1: margin.left, y1: gridY, x2: width - margin.right, y2: gridY,
      class: "chart-grid-line",
    }));
    const label = createSvgElement("text", {
      x: margin.left - 12, y: gridY + 4, "text-anchor": "end", class: "chart-axis-label",
    });
    label.textContent = `${formatAxisValue(gridValue)} ${elementDefinition.unit}`;
    chartGroup.append(label);
  }

  for (const hour of [1, 6, 12, 18, 24]) {
    const label = createSvgElement("text", {
      x: x(hour), y: height - 16, "text-anchor": "middle", class: "chart-axis-label",
    });
    label.textContent = `${hour}時`;
    chartGroup.append(label);
  }

  const contiguousSegments = splitIntoContiguousSegments(points);
  for (const segment of contiguousSegments) {
    if (segment.length > 1) {
      chartGroup.append(createSvgElement("polyline", {
        points: segment.map((point) => `${x(point.hour)},${y(point.value)}`).join(" "),
        class: "chart-line",
      }));
    }
  }

  for (const point of points) {
    const isSelected = point.hour === state.selectedHour;
    const circle = createSvgElement("circle", {
      cx: x(point.hour), cy: y(point.value), r: isSelected ? 6 : 3.5,
      class: isSelected ? "chart-point chart-point--selected" : "chart-point",
    });
    const title = createSvgElement("title");
    title.textContent = `${point.hour}時：${point.value} ${elementDefinition.unit}`;
    circle.append(title);
    chartGroup.append(circle);
  }

  elements.dailyChart.append(chartGroup);
}

function splitIntoContiguousSegments(points) {
  const segments = [];
  let currentSegment = [];
  for (const point of points) {
    const previousPoint = currentSegment.at(-1);
    if (previousPoint && point.hour !== previousPoint.hour + 1) {
      segments.push(currentSegment);
      currentSegment = [];
    }
    currentSegment.push(point);
  }
  if (currentSegment.length) segments.push(currentSegment);
  return segments;
}

function formatAxisValue(value) {
  if (Math.abs(value) >= 100) return value.toFixed(0);
  if (Math.abs(value) >= 10) return value.toFixed(1);
  return value.toFixed(2);
}

function createSvgElement(tagName, attributes = {}) {
  const element = document.createElementNS("http://www.w3.org/2000/svg", tagName);
  for (const [name, value] of Object.entries(attributes)) {
    element.setAttribute(name, value);
  }
  return element;
}


/* ==========================================
   Start application
========================================== */

initializeApplication();
