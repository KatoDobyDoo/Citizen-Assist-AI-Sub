# Citizen Assist AI — Guia Digital de Orientação Cidadã

**Global Solution — Atividade Substitutiva — Citizen Tech**  
**Aluna:** Camila Kato de Godoi  
**RM:** 570229 | **Turma:** 1CCOA — FIAP  

---

## 1. Descrição do Problema e Público Beneficiado
Muitas pessoas têm dificuldade para encontrar respostas confiáveis e diretas sobre direitos básicos no dia a dia, tanto nas relações de trabalho quanto nas relações de consumo. As informações costumam estar espalhadas em diferentes portais, escritas em linguagem jurídica complicada ou misturadas com notícias desatualizadas.

O **Citizen Assist AI** foi desenvolvido individualmente como um guia digital simples e verificável. O público beneficiado são trabalhadores em regime CLT e consumidores comuns que precisam consultar regras rápidas — como funcionamento de escalas de trabalho (5x2 e 6x1), seguro-desemprego, FGTS, arrependimento em compras online ou cancelamento de serviços — sem precisar fornecer dados pessoais e com acesso claro às fontes oficiais.

---

## 2. Temas Escolhidos e Fontes Consultadas
A base de conhecimento contém **10 orientações verificadas**, divididas em **2 temas**:
* **Direitos Trabalhistas (5 registros):** Jornada de trabalho e discussão sobre escala 5x2/6x1, seguro-desemprego, saque-rescisão vs. saque-aniversário do FGTS, prazo de férias e abono salarial PIS/PASEP.
* **Direitos do Consumidor (5 registros):** Direito de arrependimento em compras online, cobrança indevida em fatura, cancelamento de serviços de telecomunicações, Tarifa Social de Energia Elétrica e bloqueio de telemarketing.

**Fontes oficiais consultadas:** Portal Gov.br (Ministério do Trabalho e Emprego), Consolidação das Leis do Trabalho (CLT), Caixa Econômica Federal (FGTS), Código de Defesa do Consumidor (CDC), Procon, Consumidor.gov.br, Anatel, ANEEL e plataforma Não Me Perturbe.

---

## 3. Estrutura da Base de Dados e Lógica de Busca
Os registros ficam armazenados em `data/base.json`, permitindo atualizar ou adicionar novas orientações sem mexer na lógica de consulta em `src/sistema.py`.

* **Campos de cada registro:** `codigo`, `tema`, `pergunta`, `palavras_chave`, `orientacao_resumida`, `orientacao_passos`, `fonte` e `data_verificacao`.
* **Estruturas de dados:** Listas e dicionários em Python para carregar, filtrar e ordenar os dados em memória.
* **Critério de busca e ordenação:** O texto digitado pelo usuário é padronizado em minúsculas e comparado com a lista de `palavras_chave` de cada registro. Cada correspondência soma 1 ponto de relevância, e o sistema exibe até **3 sugestões ordenadas** da maior para a menor pontuação.
* **Regras de validação e limites:** Condições booleanas tratam entradas vazias, opções numéricas inválidas, arquivos ausentes e buscas sem correspondência. Quando não há resposta na base, o sistema informa sua limitação sem inventar informações.

---

## 4. Modelos de Resposta e Comparação
O sistema oferece dois formatos de apresentação para qualquer orientação encontrada:
1. **Formato Resumido:** Entrega a resposta direta em um único parágrafo curto com a fonte e a data de verificação.
2. **Formato Passo a Passo:** Organiza a orientação em etapas numeradas (1, 2, 3, 4) para facilitar a execução prática pelo cidadão.

Na comparação executada com 3 perguntas da base (Opção 3 do menu), o **Formato Passo a Passo** mostrou-se mais claro para dúvidas que exigem ação prática (como solicitar o seguro-desemprego ou devolver uma compra online), enquanto o **Formato Resumido** funcionou melhor para consultas rápidas de conceito.

---

## 5. Testes, Métricas e Melhorias Propostas
A Opção 4 do menu executa automaticamente **10 perguntas de teste** (consultas diretas, variações de termos e uma pergunta fora da base) mais **3 cenários de falha** (entrada vazia, tema inexistente e dúvida sem resposta):
* **Taxa de acerto:** 100.0% (10/10 cenários validados corretamente).
* **Tempo médio de consulta:** ~0.12 ms por busca.
* **Exemplos de consultas e sugestões:** Pesquisar por `"cancelar internet"` retorna `CONS-03` e `CONS-01` ordenados pela quantidade de palavras-chave encontradas; pesquisar por `"passaporte"` aciona o aviso de limitação da base.

**Melhorias futuras:** Adicionar suporte a sinônimos e acentuação automática na busca e permitir exportar o histórico de consultas da sessão em arquivo `.txt`.

---

## 6. Cuidados Éticos e Privacidade
* O sistema funciona localmente no terminal e **não solicita CPF, nome, telefone ou qualquer dado pessoal**.
* Toda resposta exibe explicitamente a fonte oficial, a data de verificação e o aviso de que o protótipo é informativo e **não representa um canal oficial** de órgãos públicos.

---

## 7. Como Executar e Links Obrigatórios
No terminal, dentro da pasta raiz do projeto, execute:
```bash
python src/sistema.py