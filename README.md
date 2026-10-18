# Estratégia de Negócio — A Arte da Guerra

Skill para o [Claude Code](https://claude.com/claude-code) que aplica os princípios de *A Arte da Guerra* (Sun Tzu) a situações reais de negócio: negociação, concorrência, disputa contratual, licitação, venda, conflito com fornecedor ou sócio e entrada em mercado.

![Mapa mental — A Arte da Guerra](assets/mapa_mental_arte_da_guerra.png)

Versão vertical para celular: [`assets/mapa_mental_arte_da_guerra_celular.png`](assets/mapa_mental_arte_da_guerra_celular.png) (1080 px de largura).
Para imprimir: [`assets/mapa_mental_arte_da_guerra_A3.pdf`](assets/mapa_mental_arte_da_guerra_A3.pdf) (A3 paisagem, vetorial — imprimir em tamanho real).

## O que a skill faz

| Pedido | Resultado |
|---|---|
| "mapa mental da arte da guerra" | Mapa dos 13 capítulos (Mermaid) |
| "explica o capítulo 6" | Ideias centrais + 2 aplicações em negócios |
| "estratégia para renegociar com o fornecedor X" | Análise estratégica em 5 passos |
| "analisa a disputa entre A e B" / eleição | **Modo observador**: os 5 passos aplicados aos dois lados, de forma simétrica e sem tomar partido |

### Análise em 5 passos

1. **5 fatores** (cap. 1) — Caminho, Céu, Terra, Comandante e Método, comparando os dois lados
2. **Conhecer o inimigo e a si mesmo** (cap. 3 e 13) — o que se sabe e o que falta saber
3. **Vencer sem lutar** (cap. 3) — acordo antes de confronto; litígio como último recurso
4. **Posição e manobra** (cap. 4–8) — proteger-se primeiro, depois explorar a fraqueza do outro lado
5. **Plano** — 3 a 5 ações com capítulo de origem, prazo e risco

"Engano", em negócios, significa não revelar a própria posição — nunca mentir ou agir ilegalmente.

## Instalação

Copie a pasta da skill para o diretório de skills do Claude Code:

```bash
git clone https://github.com/cesarsgobero-prog/estrategia-negocio-arte-da-guerra.git
cp -r estrategia-negocio-arte-da-guerra/skills/arte-da-guerra ~/.claude/skills/
```

No Windows (PowerShell):

```powershell
git clone https://github.com/cesarsgobero-prog/estrategia-negocio-arte-da-guerra.git
Copy-Item -Recurse estrategia-negocio-arte-da-guerra\skills\arte-da-guerra "$env:USERPROFILE\.claude\skills\"
```

Depois, no Claude Code: `/arte-da-guerra` ou peça "o que Sun Tzu faria nessa negociação?".

## Estrutura

```
skills/arte-da-guerra/
  SKILL.md                    # instruções da skill
  references/mapa-mental.md   # mapa dos 13 capítulos + tradução para negócios
assets/                       # mapa mental em PNG e SVG (horizontal e celular) + PDF A3
scripts/gerar_mapa.py         # gera o SVG/PNG (Python + Chrome headless)
```

Para regerar a imagem: `python scripts/gerar_mapa.py` (requer Google Chrome; ajuste o caminho em `CHROME` se necessário).

## Fonte

*A Arte da Guerra* está em domínio público (tradução inglesa de Lionel Giles, 1910 — [Project Gutenberg](https://www.gutenberg.org/ebooks/132)). Os textos deste repositório são resumos próprios, não transcrição.

## Licença

MIT — veja [LICENSE](LICENSE).
