## ArcPay Landing + Docs

**Установка:**

```
python -m venv venv
pip install mkdocs-material
pip install mkdocs-static-i18n
```

Файлы \*.md лежат в папке /docs/

Локализация идет по суффиксу:

```
quick-start.en.md
quick-start.ru.md
```

**Config ( mkdocs.yml )**

```yml
site_name: ArcPay
theme:
  name: material
  features:
    - content.code.copy
  logo: ../assets/logo.png
  favicon: ../assets/logo.png
  language: en

markdown_extensions:
  - pymdownx.highlight:
      anchor_linenums: true
      line_spans: __span
      pygments_lang_class: true
  - pymdownx.inlinehilite
  - pymdownx.snippets
  - pymdownx.superfences

plugins:
  - i18n:
      docs_structure: suffix
      languages:
        - locale: en
          default: true
          name: English
          build: true
          fixed_link: /doc/
        - locale: ru
          name: Русский
          build: true
          fixed_link: /doc/ru
  - search
```

Если не нужен поиск по документации - убрать "- search" из plugins.

**Сборка:**

```
mkdocs build -d doc
```

Создается папка "/doc/" с статической документацией.

После сборки требуется скопировать "index.temp.html" из корня в папку "/doc/" и переименовать в "index.html" (это костыль для редиректа, т.к. MkDocs очень хочет index.md в качестве стартовой страницы, а в нашем случае с мультиязычностью все немного ломается).

---

index.html в корневой директории - landingPage.

В лэндинг пришлось добавить костыль для ссылки на документацию, т.к. скрипт, который через JS генерирует эту ссылку лежит на стороне Framer и прибито гвоздями: ( \<link
rel="modulepreload"
fetchpriority="low"
href="https://framerusercontent.com/sites/4htJ9FTEmZ11W88SUjekUd/HZefqZauw26a3tIxbj6Zkx_IsBV6ybTybwrxZE_DuNU.OYG65MTW.mjs"
\/\> )

```html
<script>
  const DOCS_ULR = "/doc/";
  setTimeout(() => {
    document.querySelector(".framer-RrBPL").setAttribute("href", DOCS_ULR);
  }, 500);
</script>
```
