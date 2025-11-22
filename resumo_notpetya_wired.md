# Resumo Detalhado: A História Não Contada do NotPetya
**(Baseado no artigo de Andy Greenberg para a WIRED)**

> **Contexto:** O artigo narra os eventos de 27 de junho de 2017, quando o malware **NotPetya** foi lançado. Embora o alvo fosse a Ucrânia, o ataque saiu de controle e tornou-se o ciberataque mais devastador e caro da história, paralisando gigantes globais como a Maersk.

---

## 1. O Marco Zero: O Colapso da Maersk
O texto começa descrevendo o caos na sede da **A.P. Møller-Maersk** em Copenhague.
*   **O Evento:** Numa tarde de verão, as telas dos computadores começaram a ficar pretas ou exibir mensagens em vermelho exigindo resgate em Bitcoin ($300).
*   **A Propagação:** O malware se espalhou com velocidade aterrorizante. Funcionários corriam pelos corredores gritando para desligarem as máquinas, mas já era tarde.
*   **O Impacto Imediato:** A rede global da Maersk (responsável por quase 20% do transporte marítimo mundial) foi aniquilada. Telefones, e-mails e sistemas de gerenciamento de portos pararam. Caminhões ficaram parados em filas quilométricas em portos como o de Nova Jersey, sem poder entregar ou retirar cargas.

---

## 2. A Origem: Ucrânia e o Software M.E.Doc
Apesar do impacto global, o ataque foi um ato de **Ciberguerra focado na Ucrânia**.
*   **Localização:** O "Paciente Zero" foi a **Linkos Group**, uma pequena empresa de software em Kiev.
*   **O Vetor:** Eles produzem o **M.E.Doc**, um software de contabilidade usado por quase todas as empresas que pagam impostos na Ucrânia.
*   **A Invasão:** Hackers militares russos (grupo **Sandworm**) sequestraram os servidores de atualização do M.E.Doc. Eles usaram essa "porta dos fundos" para enviar o malware disfarçado de atualização de software para milhares de PCs.

---

## 3. O Malware: NotPetya
O NotPetya foi uma arma cibernética projetada para destruição rápida e irreversível.
*   **Arsenal Técnico:** O malware combinou duas ferramentas poderosas:
    1.  **EternalBlue:** Um exploit da NSA (vazado anteriormente) que aproveitava uma falha no Windows para se espalhar sem interação do usuário.
    2.  **Mimikatz:** Uma ferramenta que roubava senhas da memória RAM.
    *   *Resultado:* Se um computador fosse infectado, o malware roubava as credenciais e as usava para infectar todas as outras máquinas da rede, mesmo as que tinham o patch de segurança do Windows.
*   **Natureza:** Parecia um *ransomware* (Petya), mas era um **Wiper**. O objetivo não era ganhar dinheiro, mas destruir dados. Ele criptografava o *Master Boot Record* (MBR) de forma irreversível. Não existia chave de descriptografia.

---

## 4. A Escala da Devastação
O ataque foi descrito como "usar uma bomba nuclear para obter uma pequena vitória tática".
*   **Danos Totais:** Estimados em mais de **US$ 10 bilhões** pela Casa Branca.
*   **Vítimas Globais:**
    *   **Maersk (Transporte):** US$ 300 milhões de prejuízo. Teve que reinstalar 4.000 servidores e 45.000 PCs.
    *   **Merck (Farmacêutica):** US$ 870 milhões. Perdeu capacidade de fabricar vacinas temporariamente.
    *   **FedEx (TNT Express):** US$ 400 milhões.
    *   **Saint-Gobain (Construção):** US$ 384 milhões.
    *   **Mondelēz (Alimentos):** US$ 188 milhões.
*   **Impacto na Ucrânia:** Bancos, aeroportos, metrô e até os sistemas de monitoramento de radiação de **Chernobyl** foram derrubados.

---

## 5. A Recuperação da Maersk (O "Milagre" de Gana)
A recuperação da Maersk foi uma operação de guerra baseada em Maidenhead, Inglaterra.
*   **O Problema Crítico:** A Maersk tinha backups de dados, mas perdeu todos os seus **Controladores de Domínio** (os servidores que mapeiam a rede e gerenciam acessos). Sem eles, não podiam restaurar nada. Como os controladores sincronizavam entre si, o malware limpou todos simultaneamente.
*   **A Salvação:** Em um escritório remoto em **Gana**, um Controlador de Domínio sobreviveu porque **houve um apagão de energia** local antes do ataque, deixando a máquina offline.
*   **A Missão:** A internet em Gana era lenta demais para enviar o backup. Um funcionário voou de Gana para a Nigéria e depois para Londres carregando o disco rígido físico. Esse disco foi a chave para reconstruir toda a infraestrutura global da empresa.

---

## 6. Conclusão e Lições
*   **Atribuição:** O ataque foi atribuído ao exército russo (GRU), como parte da guerra híbrida contínua contra a Ucrânia.
*   **Danos Colaterais:** O NotPetya provou que no ciberespaço não existem fronteiras. Um ataque direcionado a Kiev atingiu hospitais na Pensilvânia e fábricas na Tasmânia em minutos.
*   **Interconectividade:** A infraestrutura global é frágil. Uma falha em um software de contabilidade ucraniano paralisou portos ao redor do mundo, interrompendo cadeias de suprimentos vitais (alimentos, remédios, peças).
*   **Mensagem Política:** Especialistas argumentam que a Rússia sabia que o ataque se espalharia, servindo como punição para qualquer empresa ocidental que fizesse negócios com a Ucrânia.

---
