from playwright.sync_api import sync_playwright
import pandas as pd
import time


def safe_text(locator):
    try:
        return locator.inner_text().strip()
    except:
        return ""


def extrair_campo(page, label_texto):
    try:
        label = page.locator(f"label:text-is('{label_texto}:')")
        linha = label.locator("xpath=ancestor::tr")
        tds = linha.locator("td")

        if tds.count() >= 2:
            return safe_text(tds.nth(1))

        return ""
    except:
        return ""


def extrair_metodologia(page):
    try:
        label = page.locator(
            "label:text-is('Metodologia de pesquisa:')"
        )

        texto = (
            label.locator(
                "xpath=ancestor::tr/following-sibling::tr[1]/td"
            )
            .inner_text()
            .strip()
        )

        return texto

    except:
        return ""


def extrair_contratante(page):
    try:
        label = page.locator(
            "label:text-is('Contratante(s):')"
        )

        linha = label.locator("xpath=ancestor::tr")
        tds = linha.locator("td")

        if tds.count() >= 2:
            return safe_text(tds.nth(1))

        return ""

    except:
        return ""


dados = []

with sync_playwright() as p:

    browser = p.chromium.launch(
        headless=False,
        slow_mo=300
    )

    page = browser.new_page()

    page.goto(
        "https://pesqele-divulgacao.tse.jus.br/app/pesquisa/listar.xhtml",
        wait_until="networkidle"
    )

    print("Página aberta")

    # Seleciona Eleições Gerais 2026
    page.select_option(
        "#formPesquisa\\:eleicoes_input",
        value="81"
    )

    # Seleciona Brasil
    page.select_option(
        "#formPesquisa\\:filtroUF_input",
        value="BR"
    )

    # Clica em Pesquisar
    page.click("text=Pesquisar")

    page.wait_for_timeout(3000)

    for pagina in range(1, 6):

        print(f"\nPágina {pagina}")

        page.wait_for_timeout(2000)

        linhas = page.locator(
            "a[id*=':detalhar']"
        )

        quantidade = linhas.count()

        print(f"{quantidade} pesquisas")

        for i in range(quantidade):

            try:

                detalhe_id = (
                    f"formPesquisa:tabelaPesquisas:{i}:detalhar"
                )

                print(f"Pesquisa {i+1}")

                page.locator(
                    f"a[id='{detalhe_id}']"
                ).click()

                page.wait_for_load_state("networkidle")

                registro = {
                    "numero_identificacao": extrair_campo(
                        page,
                        "Número de identificação"
                    ),
                    "data_divulgacao": extrair_campo(
                        page,
                        "Data de divulgação"
                    ),
                    "empresa_contratada": extrair_campo(
                        page,
                        "Empresa contratada/ Nome Fantasia"
                    ),
                    "entrevistados": extrair_campo(
                        page,
                        "Entrevistados"
                    ),
                    "data_inicio": extrair_campo(
                        page,
                        "Data de início da pesquisa"
                    ),
                    "data_termino": extrair_campo(
                        page,
                        "Data de término da pesquisa"
                    ),
                    "contratantes": extrair_contratante(page),
                    "metodologia": extrair_metodologia(page)
                }

                print(
                    registro["numero_identificacao"]
                )

                dados.append(registro)

                page.go_back()

                page.wait_for_load_state(
                    "networkidle"
                )

            except Exception as e:
                print("Erro:", e)

        # próxima página

        if pagina < 5:

            try:
                page.locator(
                    f"text='{pagina+1}'"
                ).click()

                page.wait_for_timeout(3000)

            except Exception as e:
                print("Erro paginação:", e)

    browser.close()

df = pd.DataFrame(dados)

df.to_csv(
    "pesquisas_brasil_2026.csv",
    index=False,
    encoding="utf-8-sig"
)

print(
    f"\nConcluído. {len(df)} pesquisas salvas."
)
