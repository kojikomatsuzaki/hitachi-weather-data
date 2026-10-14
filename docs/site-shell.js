/* Shared site chrome. No observation-data logic lives here. */
(() => {
  const scriptUrl = new URL(document.currentScript.src);
  const root = new URL("./", scriptUrl);
  const preview = document.body.dataset.page === "preview";
  const href = (path) => new URL(path, root).href;
  const header = document.getElementById("site-header-slot");
  const footer = document.getElementById("site-footer-slot");
  if (!header || !footer) return;

  const nav = `<nav class="site-nav" aria-label="サイト内ナビゲーション">
    <a href="${href("index.html")}"${!preview ? ' aria-current="page"' : ""}>観測データ</a>
    <a href="${href("preview/")}"${preview ? ' aria-current="page"' : ""}>試作プレビュー</a>
    <a href="https://github.com/kojikomatsuzaki/hitachi-weather-data/blob/main/docs/collection-policy.md">採録方針</a>
  </nav>`;
  header.outerHTML = `<header class="site-header">
    <div class="site-header__inner">
      <p class="site-header__eyebrow">Hitachi Weather Data Archive</p>
      <div class="site-header__title-row">
        <h1>日立市天気相談所<br class="mobile-break"> 観測データアーカイブ</h1>
        <span class="publication-badge">${preview ? "試作プレビュー・正式版ではありません" : "非公式・観測データアーカイブ"}</span>
      </div>
      <p class="site-header__description">
        日立市天気相談所（気象庁予報業務許可第2号）が公表した、1953年以降の日立市役所観測所の「気象観測データ」を、原資料の観測値・表記を変更することなく収録し、順次公開しています。
        <a href="https://tenki.city.hitachi.lg.jp/obs/contents/919">出典：日立市天気相談所「気象観測データ」</a>
      </p>
      ${preview ? '<p class="site-preview-note">このページは表示・操作を検証する試作版です。</p>' : ""}
      ${nav}
    </div>
  </header>`;
  footer.outerHTML = `<footer class="site-footer">
    <div class="site-footer__inner">
      <p>本サイトは日立市天気相談所の公式サイトではありません。原資料の公表主体と、本アーカイブの運営主体は異なります。</p>
      <p>アーカイブ制作・運営：Hiroshi Komatsuzaki</p>
      <p><a href="https://tenki.city.hitachi.lg.jp/obs/contents/919">原資料</a> · <a href="https://github.com/kojikomatsuzaki/hitachi-weather-data">GitHubリポジトリ</a> · <a href="https://github.com/kojikomatsuzaki/hitachi-weather-data/blob/main/docs/collection-policy.md">採録方針</a></p>
    </div>
  </footer>`;
})();
