# Portfolio audit — 20 September 2026

Audited all 21 HTML pages, the shared header/footer fragments, local CSS and JavaScript, image references, downloadable document paths, and Webflow lightbox data. The existing dark palette, typography, hero image, project order, and minimal presentation were preserved. Changes are local; nothing was deployed.

## Implementation verdict

The portfolio has a coherent visual identity. Its main weaknesses were repeated copy/paste errors and stale Webflow export content, rather than a need for redesign. The mechanical design detector reported font-choice warnings and eight skipped-heading findings. Font warnings were deliberately dismissed because the brief preserves the existing typography; the heading findings were corrected without changing their visual sizes.

Indicative post-touchup health score (manual assessment, not WCAG certification):

| Dimension | Score | Evidence and limits |
| --- | --- | --- |
| Accessibility | 3/4 | Added language, landmarks, skip link, focus styles, image names and heading order. Full screen-reader and contrast certification remain outside this pass. |
| Performance | 3/4 | Existing lazy loading retained; gallery image dimensions reserve space. Large full-resolution artwork and external font/script requests remain. |
| Responsive design | 3/4 | All pages fit tested 390px and desktop viewports; homepage also fits 320px and 768px. Not an exhaustive device matrix. |
| Theming | 1/4 | Intentional single dark theme, with mostly hardcoded legacy colors. A token migration would be a separate refactor, not a necessary touchup. |
| Implementation integrity | 3/4 | Local paths and document structure pass checks; ambiguous certificate mappings still need content confirmation. |
| **Total** | **13/20** | Functional cleanup complete; content verification and legacy maintainability remain. |

## Fixed findings

| Priority | Finding and location | Change |
| --- | --- | --- |
| P1 | Achievements navigation broken on all 15 `portfolio/*.html` pages | Corrected the parent-directory path. |
| P1 | Fixed 300px tiles could exceed the tablet container in `css/folio.css` | Fluid desktop tiles, two columns at tablet widths, original single-column mobile presentation. |
| P1 | Contact form implied sending but depended on a mail application | Explicit “OPEN EMAIL APP” action and explanation; encoded subject/body, required email/message, autocomplete, direct email fallback. No backend or delivery claim. |
| P2 | Footer image paths wrong on six root pages | Corrected relative paths. |
| P2 | Branding links pointed to `#` | Home links and accessible names added. |
| P2 | Missing document language, landmarks, keyboard skip target and visible focus treatment | Applied across all pages. |
| P2 | Misleading homepage image labels and unnamed gallery images | Corrected project labels and added filename-grounded image names. Gallery art could still benefit from authored descriptions. |
| P2 | Stale page titles/social titles; BRANSOL heading incorrectly said Abundant Life | Corrected titles, added page descriptions, corrected BRANSOL and obvious spelling errors. |
| P2 | Repeated grid IDs on seven project pages | Removed duplicate IDs; existing single-cell grid placement preserved. |
| P2 | Gallery images had no intrinsic dimensions | Added actual width/height and asynchronous decoding; preserved natural aspect ratio. |
| P2 | Empty CMS template pages and missing template CSS | Replaced unused template bodies with a portfolio link, corrected stylesheet path, added `noindex`. |
| P2 | Skipped heading levels and poorly contrasted form placeholders | Corrected heading levels while preserving sizes; lightened placeholders. |
| P3 | Hover zoom ignored reduced-motion preference | Added targeted reduced-motion rules. |
| P3 | CV link label said 2022 while targeting the 2024 file | Matched label to the existing filename; did not change the CV. |
| P3 | Stale Achievements URL in unused header fragment | Corrected the fragment for future reuse. |

## Remaining content and maintenance findings

1. **P1 — Certificate destinations need confirmation (`downloads.html`).** “Ignition - Data Literacy” points to the Leadership PDF. Six other labels (Project Management Fundamentals, Digital Marketing, Digital Marketing Strategy, Digital Transformation, Jellyfish Digital Marketing, and Deloitte Keep Data Safe) all point to the same Future Now image. These URLs exist, but the labels may not describe the linked certificate. Existing links were retained because replacement documents cannot be inferred. Supply or identify the correct certificates before publishing a refreshed achievements page.
2. **P2 — Biography and dated claims (`about.html`, `portfolio/amara.html`, footer).** The biography contains malformed sentences and dated employment/experience statements; Amara says its ecommerce site is currently in progress. The footer still says 2024. Confirm current facts during a content refresh. No employment, experience, completion, or qualification claims were invented.
3. **P2 — External runtime dependencies.** Existing Webflow interactions require externally loaded jQuery; fonts also depend on remote services. A later dependency update/self-hosting pass should regression-test the mobile menu and lightboxes. This audit did not assess third-party vulnerability databases or upgrade the generated bundle. Lightbox anchors now have real image URLs as a fallback.
4. **P2 — Large artwork.** Several full-resolution project images are 1–1.9 MB; the hero JPEG is about 754 KB. Lazy loading limits initial gallery costs. A separately reviewed image-compression pass could reduce transfer size while checking design-detail fidelity. No source artwork was recompressed.
5. **P2 — Gallery accessibility polish.** Filename-grounded alt text is a baseline; detailed artwork descriptions require editorial review. The legacy lightbox closes with Escape, but robust keyboard focus restoration should be assessed in a future accessibility pass.
6. **P3 — Legacy CSS duplication.** Many generated grid selectors and hardcoded colors remain. Consolidating them is optional and would be a broader refactor than requested.

## Validation

- `python3 scripts/audit_site.py`: **21 pages, 1,020 local references, zero errors**. Checks include HTML references, `srcset`, CSS resources, JSON gallery URLs, duplicate IDs, language, one main/H1/title, and fragment targets.
- Browser DOM checks on every page at desktop width (1,440px) and mobile width (390px): no horizontal overflow; no failed completed images observed. Lazy images outside the viewport were verified through file-reference checks, not all forced to load.
- Homepage at 768px: two columns, no horizontal overflow. At 320px: no horizontal overflow.
- Mobile menu opens and its Achievements link navigates successfully.
- Representative Division lightbox opens; Escape closes it. No claim of exhaustive testing of every gallery interaction.
- Skip link transfers focus to `main-content` after the existing Webflow scroll completes.
- Contact composer checked with isolated Node mocks: special characters/newlines correctly encoded; invalid form does not open an email URL. No email was opened or sent. Real delivery depends on the visitor's configured email app and was not tested.
- Desktop homepage and mobile homepage/contact visually inspected; browser viewport override reset afterward.
- External destination availability, actual PDF contents, full screen-reader behavior, and every browser/device combination were not validated.

A pre-edit backup of touched original files is stored at `/tmp/beau-folio-before-audit.zip`. The project was not a Git repository. Use `scripts/audit_site.py` after future edits to catch local link regressions.
