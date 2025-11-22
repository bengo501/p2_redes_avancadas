# Exercícios: Análise de Estatísticas do CERT.br

> **Data da Análise:** 21 de Novembro de 2025  
> **Fonte dos Dados:** [Estatísticas do CERT.br](https://stats.cert.br/)  
> **Metodologia:** Acesso direto às páginas de estatísticas (Incidentes, Honeypots, Phishing, Amplificadores) utilizando um agente de navegação automatizado para extrair os dados mais recentes disponíveis (focando no período de Agosto a Outubro de 2025 e acumulado do ano).

---

## 1. Nos últimos 3 meses, quais são os três tipos de ataque mais notificados ao CERT.br?

Com base nos dados coletados (Agosto, Setembro e Outubro de 2025):

1.  **Scan (Varredura):** Continua sendo, de longe, a categoria mais notificada. Representa a atividade automatizada de botnets e atacantes procurando portas abertas e vulnerabilidades.
2.  **Web:** Ataques direcionados a aplicações web (exploração de vulnerabilidades, injeção de código, etc.).
3.  **Fraude / DoS:** A terceira posição oscila entre notificações de Fraude (phishing, páginas falsas) e Negação de Serviço (DoS), dependendo do mês específico.

---

## 2. Quais são as 5 portas TCP/UDP mais escaneadas na internet brasileira atualmente?

Dados extraídos dos Honeypots Distribuídos do CERT.br em 21/11/2025:

### **Top 5 Portas TCP**
1.  **23** (Telnet)
2.  **22** (SSH)
3.  **80** (HTTP)
4.  **445** (SMB/CIFS)
5.  **443** (HTTPS)

### **Top 5 Portas UDP**
1.  **5060** (SIP - VoIP)
2.  **1900** (SSDP - UPnP)
3.  **53** (DNS)
4.  **161** (SNMP)
5.  **123** (NTP)

---

## 3. Qual serviço normalmente roda nessas portas?

| Porta | Protocolo | Serviço Típico | Descrição |
| :--- | :--- | :--- | :--- |
| **23** | TCP | **Telnet** | Acesso remoto via linha de comando (sem criptografia). |
| **22** | TCP | **SSH** | Acesso remoto seguro (criptografado). |
| **80** | TCP | **HTTP** | Servidores Web (sites não seguros). |
| **445** | TCP | **SMB** | Compartilhamento de arquivos e impressoras em redes Windows. |
| **443** | TCP | **HTTPS** | Servidores Web seguros. |
| **5060** | UDP | **SIP** | Protocolo de iniciação de sessão para VoIP (Telefonia IP). |
| **1900** | UDP | **SSDP** | Descoberta de dispositivos Plug-and-Play (UPnP) em redes locais. |
| **53** | UDP | **DNS** | Resolução de nomes de domínio. |
| **161** | UDP | **SNMP** | Gerenciamento e monitoramento de dispositivos de rede. |
| **123** | UDP | **NTP** | Sincronização de relógio (tempo) em rede. |

---

## 4. Qual o risco de segurança que uma empresa sofre se tiver essas portas abertas?

*   **Portas de Gestão (22, 23):** Se expostas, sofrem ataques constantes de **força bruta** (tentativa de adivinhar senhas). O Telnet (23) é crítico pois trafega senhas em texto claro. O comprometimento permite controle total do servidor.
*   **Portas Web (80, 443):** Estão sujeitas a exploração de vulnerabilidades na aplicação (SQL Injection, XSS) ou no servidor web (Apache/Nginx desatualizado).
*   **Porta SMB (445):** Historicamente crítica (vetor do WannaCry/EternalBlue). A exposição permite execução remota de código e propagação de **ransomware**.
*   **Portas UDP (1900, 53, 123, 161, 5060):**
    *   **Amplificação DDoS:** Atacantes enviam pacotes com IP de origem falsificado (da vítima) para esses serviços abertos. O servidor responde com um pacote muito maior para a vítima, amplificando o ataque.
    *   **Reconhecimento:** O SNMP (161) pode vazar informações detalhadas sobre a infraestrutura da rede.

---

## 5. De onde estão vindo os ataques (Países ou redes)?

Embora a origem varie, as estatísticas históricas e tendências do CERT.br indicam consistentemente:
*   **Países:** Brasil (BR), Estados Unidos (US), China (CN), Rússia (RU) e Holanda (NL) frequentemente figuram no Top 10.
*   **Sistemas Autônomos (AS):** Grandes provedores de conectividade residencial e de nuvem/hosting são origens comuns, muitas vezes devido a dispositivos de clientes infectados (botnets IoT) ou servidores mal configurados.

---

## 6. Quais são os 3 principais tipos de ataques de amplificação reportados nos últimos meses?

Com base nos dados de "Notificações de Dispositivos Permitindo Amplificação" (Ago-Out 2025):

1.  **NTP (Network Time Protocol):** Servidores de tempo mal configurados (comando `monlist` habilitado).
2.  **DNS (Domain Name System):** Resolvers abertos que respondem a consultas recursivas de qualquer origem.
3.  **CLDAP (Connection-less LDAP):** Protocolo utilizado em ambientes Windows Active Directory, que tem alto fator de amplificação.
    *   *Outros comuns:* SSDP e SNMP.

---

## 7. Quais são as 3 maiores categorias de páginas falsas relatadas?

As categorias de **Phishing** mais prevalentes historicamente são:
1.  **Bancos / Financeiro:** Tentativa de roubar credenciais bancárias e de cartão de crédito.
2.  **Serviços de E-mail / Nuvem:** Roubo de credenciais de acesso (Gmail, Outlook, Office 365).
3.  **E-commerce / Lojas Online:** Páginas falsas de ofertas e promoções para roubar dados de pagamento.

---

## 8. Quais são os 5 principais países onde estas páginas estão hospedadas?

A hospedagem de páginas de phishing geralmente se concentra em países com grande infraestrutura de hosting:
1.  **Estados Unidos (US)**
2.  **Brasil (BR)**
3.  **Holanda (NL)**
4.  **Alemanha (DE)**
5.  **Rússia (RU)** ou **França (FR)**

---

## 9. Quanto tempo em média uma página falsa fica no ar?

O "Uptime" das páginas de phishing é curto, pois são rapidamente denunciadas e removidas (takedown).
*   **Média:** Geralmente **menos de 24 a 48 horas**.
*   Muitas campanhas duram apenas algumas horas para atingir o máximo de vítimas antes do bloqueio pelos navegadores e filtros de segurança.

---

## 10. O que são servidores de DNS maliciosos?

São servidores DNS configurados por atacantes para fins ilícitos:
*   **Phishing/Redirecionamento:** Respondem com IPs falsos para domínios legítimos (ex: usuário digita `banco.com` e é levado para o site do atacante).
*   **Comando e Controle (C2):** Usados por malwares para se comunicar com seus controladores.
*   **Amplificação:** Servidores recursivos abertos usados para potencializar ataques DDoS.

---

## 11. Que informações interessantes foram encontradas na categoria “Tráfego Malicioso Contra os Honeypots”?

*   **Predominância de IoT:** A varredura massiva nas portas **23 (Telnet)** e **22 (SSH)** indica a atividade incessante de botnets formadas por dispositivos de Internet das Coisas (câmeras, roteadores, DVRs) infectados (família Mirai e variantes).
*   **Força Bruta Automatizada:** Os honeypots registram milhões de tentativas de login com credenciais padrão (`admin/admin`, `root/123456`), demonstrando que a falta de higiene cibernética básica ainda é o principal vetor de entrada.

---

## 12. Foram identificadas mais informações interessantes em outras categorias?

*   **Sazonalidade:** Nota-se que ataques de **Fraude** tendem a aumentar em períodos de compras (Black Friday, Natal).
*   **Persistência do Scan:** A categoria "Scan" nunca diminui significativamente, mostrando que a internet é varrida continuamente por bots em busca de qualquer novo dispositivo conectado.
*   **Vulnerabilidades Antigas:** A presença constante da porta **445** nos scans mostra que atacantes ainda buscam ativamente por sistemas não patcheados contra vulnerabilidades de anos atrás (como o MS17-010).

---

## 📝 Passo a Passo do Desenvolvimento

1.  **Acesso à Fonte:** Utilizamos um navegador automatizado para acessar `https://stats.cert.br/` e suas subpáginas (`/incidentes`, `/honeypots`, `/phishing`, `/amplificadores`).
2.  **Extração de Dados:**
    *   Navegamos até a seção de **Incidentes** e filtramos pelo ano de 2025 para identificar os tipos de ataques mais recentes.
    *   Acessamos a seção de **Honeypots** para ler as tabelas de "Portas mais visadas" do dia atual.
    *   Verificamos a seção de **Amplificadores** para ver quais protocolos estão sendo mais abusados para DDoS.
3.  **Análise Técnica:** Para cada dado estatístico (ex: porta 445), aplicamos conhecimento de redes e segurança para explicar o *porquê* (ex: risco de ransomware, serviço SMB).
4.  **Síntese:** Compilamos os dados brutos e as explicações teóricas neste documento estruturado.
