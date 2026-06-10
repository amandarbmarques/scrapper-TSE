from playwright.sync_api import sync_playwright

with sync_playwright() as p:

    browser = p.chromium.launch(
        headless=False
    )

    page = browser.new_page()

    page.goto(
        "https://pesqele-divulgacao.tse.jus.br/app/pesquisa/listar.xhtml",
        wait_until="networkidle"
    )

    print("Site aberto")

    page.select_option(
        "#formPesquisa\\:eleicoes_input",
        value="81"
    )

    page.select_option(
        "#formPesquisa\\:filtroUF_input",
        value="BR"
    )

    print("Filtros preenchidos")

    page.click("text=Pesquisar")

    page.wait_for_timeout(5000)

    botoes = page.locator(
        "a[id*=':detalhar']"
    )

    print(
        f"Pesquisas encontradas: {botoes.count()}"
    )

    input(
        "\nPressione ENTER para fechar..."
    )

    browser.close()
