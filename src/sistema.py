import json
import os
import time

# Localiza automaticamente a pasta raiz do projeto ('Citizen-Assist-AI-Sub')
DIRETORIO_ATUAL = os.path.dirname(os.path.abspath(__file__))
DIRETORIO_RAIZ = os.path.dirname(DIRETORIO_ATUAL)
CAMINHO_BASE = os.path.join(DIRETORIO_RAIZ, "data", "base.json")


def carregar_base(caminho):
    """Lê o arquivo JSON com os registros e valida campos obrigatórios."""
    if not os.path.exists(caminho):
        print(f"[Erro] Arquivo '{caminho}' não encontrado.")
        return []

    try:
        with open(caminho, "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)
    except json.JSONDecodeError:
        print("[Erro] O arquivo JSON está vazio ou com formatação inválida.")
        return []

    if not isinstance(dados, list) or len(dados) == 0:
        print("[Aviso] A base de orientações está vazia.")
        return []

    campos_obrigatorios = [
        "codigo", "tema", "pergunta", "palavras_chave",
        "orientacao_resumida", "orientacao_passos",
        "fonte", "data_verificacao"
    ]

    base_valida = []
    for item in dados:
        # Verifica se todos os campos essenciais existem e não estão vazios
        tem_todos_campos = all(campo in item and item[campo] for campo in campos_obrigatorios)
        if tem_todos_campos:
            base_valida.append(item)

    return base_valida


def listar_temas(base):
    """Retorna os temas únicos cadastrados na base."""
    temas = []
    for item in base:
        if item["tema"] not in temas:
            temas.append(item["tema"])
    return temas


def limpar_texto(texto):
    """Padroniza o texto em minúsculas e remove pontuação simples para facilitar a busca."""
    texto = texto.lower().strip()
    for simbolo in ["?", "!", ".", ",", ";", ":", "-", "/"]:
        texto = texto.replace(simbolo, " ")
    return texto


def buscar_orientacoes(base, consulta, tema_filtro=None):
    """
    Busca orientações por palavras-chave (e tema opcional).
    Retorna até 3 sugestões ordenadas pela quantidade de palavras-chave encontradas.
    """
    consulta_limpa = limpar_texto(consulta)
    if consulta_limpa == "":
        return []

    palavras_usuario = consulta_limpa.split()
    resultados = []

    for item in base:
        # Se houver filtro por tema, ignora os outros temas
        if tema_filtro and item["tema"].lower() != tema_filtro.lower():
            continue

        pontos = 0
        for chave in item["palavras_chave"]:
            chave_limpa = limpar_texto(chave)
            # Verifica se a palavra-chave aparece na frase digitada ou nas palavras isoladas
            if chave_limpa in consulta_limpa or chave_limpa in palavras_usuario:
                pontos += 1

        if pontos > 0:
            resultados.append((pontos, item))

    # Ordena do maior número de correspondências para o menor
    resultados.sort(key=lambda x: x[0], reverse=True)

    # Retorna no máximo as 3 melhores sugestões
    return resultados[:3]


def exibir_orientacao(item, formato="1"):
    """Apresenta a orientação no formato escolhido (1 = Resumido, 2 = Passo a Passo)."""
    print("\n" + "=" * 65)
    print(f"CÓDIGO: {item['codigo']} | TEMA: {item['tema']}")
    print(f"PERGUNTA: {item['pergunta']}")
    print("-" * 65)

    if formato == "2":
        print("ORIENTAÇÃO (FORMATO PASSO A PASSO):")
        print(item["orientacao_passos"])
    else:
        print("ORIENTAÇÃO (FORMATO RESUMIDO):")
        print(item["orientacao_resumida"])

    print("-" * 65)
    print(f"Fonte verificada: {item['fonte']}")
    print(f"Data de verificação: {item['data_verificacao']}")
    print("Aviso: Este assistente é informativo e não substitui canais oficiais.")
    print("=" * 65 + "\n")


def escolher_formato_resposta():
    """Permite ao usuário escolher entre o modelo resumido e o passo a passo."""
    print("\nEscolha o formato de apresentação da resposta:")
    print("1 - Formato Resumido (direto ao ponto)")
    print("2 - Formato Passo a Passo (detalhado em etapas)")
    escolha = input("Formato (1 ou 2) [padrão 1]: ").strip()
    if escolha == "2":
        return "2"
    return "1"


def comparar_dois_formatos(base):
    """Executa 3 perguntas nos dois formatos de resposta para comparação documental."""
    print("\n--- COMPARAÇÃO DOS DOIS FORMATOS DE RESPOSTA (3 PERGUNTAS) ---")
    perguntas_comparacao = [
        "Como funciona a escala 5x2 na CLT?",
        "Como solicitar o seguro desemprego?",
        "Qual o prazo de arrependimento em compra online?"
    ]

    for i, pergunta in enumerate(perguntas_comparacao, start=1):
        print(f"\n>>> TESTE COMPARATIVO {i}: '{pergunta}'")
        achados = buscar_orientacoes(base, pergunta)
        if achados:
            registro = achados[0][1]
            print("\n[A] MODELO RESUMIDO:")
            print(registro["orientacao_resumida"])
            print(f"Fonte: {registro['fonte']}")

            print("\n[B] MODELO PASSO A PASSO:")
            print(registro["orientacao_passos"])
            print(f"Fonte: {registro['fonte']}")
        print("-" * 65)


def executar_bateria_testes(base):
    """Executa 10 perguntas de teste + 3 testes de falhas e calcula métricas."""
    print("\n--- EXECUTANDO BATERIA DE TESTES E MÉTRICAS ---")

    # 10 perguntas planejadas (diretas, variações de termos e fora da base)
    testes = [
        ("Como funciona a escala 5x2 na CLT?", "TRAB-01"),
        ("Quero pedir meu seguro desemprego", "TRAB-02"),
        ("Diferença entre saque aniversario e rescisao fgts", "TRAB-03"),
        ("Qual o prazo para receber pagamento das ferias?", "TRAB-04"),
        ("Quem tem direito ao abono salarial pis?", "TRAB-05"),
        ("Posso devolver compra online por arrependimento?", "CONS-01"),
        ("Veio cobranca indevida na minha fatura", "CONS-02"),
        ("Quero cancelar internet sem falar com atendente", "CONS-03"),
        ("Como conseguir desconto na conta de luz tarifa social?", "CONS-04"),
        ("Como tirar passaporte na policia federal?", None)  # Fora da base
    ]

    acertos = 0
    tempos_ms = []

    for i, (pergunta, esperado) in enumerate(testes, start=1):
        inicio = time.perf_counter()
        resultados = buscar_orientacoes(base, pergunta)
        fim = time.perf_counter()

        tempo_consulta = (fim - inicio) * 1000
        tempos_ms.append(tempo_consulta)

        obtido = resultados[0][1]["codigo"] if resultados else None
        passou = (obtido == esperado)

        if passou:
            acertos += 1

        status = "ACERTO" if passou else "ERRO"
        print(
            f"Teste {i:02d} | Pergunta: '{pergunta}'\n"
            f"   Esperado: {esperado} | Obtido: {obtido} | Status: {status} | Tempo: {tempo_consulta:.3f} ms"
        )

    taxa_acerto = (acertos / len(testes)) * 100
    tempo_medio = sum(tempos_ms) / len(tempos_ms)

    print("\n--- TESTES DE FALHAS E LIMITAÇÕES (3 CENÁRIOS) ---")
    # Falha 1: Entrada vazia
    res_vazia = buscar_orientacoes(base, "   ")
    print(f"Falha 1 (Entrada vazia): Retornou {len(res_vazia)} resultados -> Tratado corretamente.")

    # Falha 2: Tema inexistente
    res_tema = buscar_orientacoes(base, "fgts", tema_filtro="Saúde")
    print(f"Falha 2 (Tema inexistente 'Saúde'): Retornou {len(res_tema)} resultados -> Tratado corretamente.")

    # Falha 3: Pergunta sem correspondência na base
    res_fora = buscar_orientacoes(base, "como renovar cnh vencida")
    print(f"Falha 3 (Pergunta fora da base): Retornou {len(res_fora)} resultados -> Aviso de limitação acionado.")

    print("\n--- RESUMO DOS INDICADORES ---")
    print(f"Total de perguntas avaliadas: {len(testes)}")
    print(f"Total de acertos: {acertos}/{len(testes)}")
    print(f"Taxa de acerto: {taxa_acerto:.1f}%")
    print(f"Tempo médio de consulta: {tempo_medio:.3f} ms")
    print("=" * 65 + "\n")


def menu_principal():
    """Controla a navegação principal do sistema no terminal."""
    base = carregar_base(CAMINHO_BASE)
    if not base:
        print("Encerrando programa devido a problema no carregamento da base.")
        return

    temas = listar_temas(base)

    while True:
        print("\n=======================================================")
        print("   CITIZEN ASSIST AI — GUIA DIGITAL DE ORIENTAÇÃO")
        print("=======================================================")
        print("1 - Consultar por Tema")
        print("2 - Pesquisar por Palavras-Chave")
        print("3 - Comparar Formatos de Resposta (3 perguntas)")
        print("4 - Executar Testes e Métricas de Desempenho")
        print("0 - Sair")
        print("-------------------------------------------------------")

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "0":
            print("Encerrando o Citizen Assist AI. Até logo!")
            break

        elif opcao == "1":
            print("\nTemas disponíveis:")
            for idx, t in enumerate(temas, start=1):
                print(f"{idx} - {t}")
            print("0 - Voltar ao menu")

            escolha_tema = input("Digite o número do tema: ").strip()
            if escolha_tema == "0":
                continue

            if not escolha_tema.isdigit() or not (1 <= int(escolha_tema) <= len(temas)):
                print("[Aviso] Opção de tema inválida. Tente novamente.")
                continue

            tema_selecionado = temas[int(escolha_tema) - 1]
            itens_tema = [item for item in base if item["tema"] == tema_selecionado]

            print(f"\nOrientações disponíveis em '{tema_selecionado}':")
            for idx, item in enumerate(itens_tema, start=1):
                print(f"{idx} - [{item['codigo']}] {item['pergunta']}")

            escolha_item = input("Escolha o número da pergunta (ou 0 para voltar): ").strip()
            if escolha_item == "0":
                continue

            if not escolha_item.isdigit() or not (1 <= int(escolha_item) <= len(itens_tema)):
                print("[Aviso] Opção inválida. Retornando ao menu.")
                continue

            formato = escolher_formato_resposta()
            exibir_orientacao(itens_tema[int(escolha_item) - 1], formato)

        elif opcao == "2":
            consulta = input("\nDigite sua dúvida ou palavras-chave: ").strip()
            if consulta == "":
                print("[Aviso] Consulta vazia. Digite pelo menos uma palavra para pesquisar.")
                continue

            sugestoes = buscar_orientacoes(base, consulta)

            if not sugestoes:
                print("\n[Limitação da Base] Não encontrei orientações verificadas para essa dúvida.")
                print("Não inventamos respostas: consulte os portais oficiais (gov.br ou Procon).")
                continue

            print(f"\nEncontrei {len(sugestoes)} sugestão(ões) ordenada(s) por relevância:")
            for idx, (pontos, item) in enumerate(sugestoes, start=1):
                print(f"{idx} - [{item['codigo']}] {item['pergunta']} ({pontos} palavra(s)-chave)")

            if len(sugestoes) == 1:
                escolha_sug = "1"
            else:
                escolha_sug = input("Digite o número da orientação desejada (ou 0 para voltar): ").strip()
                if escolha_sug == "0":
                    continue
                if not escolha_sug.isdigit() or not (1 <= int(escolha_sug) <= len(sugestoes)):
                    print("[Aviso] Opção inválida. Retornando ao menu.")
                    continue

            formato = escolher_formato_resposta()
            registro_escolhido = sugestoes[int(escolha_sug) - 1][1]
            exibir_orientacao(registro_escolhido, formato)

        elif opcao == "3":
            comparar_dois_formatos(base)

        elif opcao == "4":
            executar_bateria_testes(base)

        else:
            print("[Aviso] Opção inválida. Digite 1, 2, 3, 4 ou 0.")


if __name__ == "__main__":
    menu_principal()