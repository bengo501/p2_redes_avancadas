# Guia do Trabalho 2: Análise de Vulnerabilidades

> **Objetivo do Trabalho:** Realizar e documentar a análise de vulnerabilidades em dois alvos reais (rede doméstica ou laboratório), identificando falhas, classificando riscos e propondo correções.

---

## 1. Conceitos Fundamentais

Para realizar este trabalho com qualidade técnica, é essencial dominar os seguintes conceitos:

### 1.1 Vulnerability Assessment vs Pentest
*   **Vulnerability Assessment (Análise de Vulnerabilidades):** É o foco deste trabalho. O objetivo é **identificar, quantificar e priorizar** (classificar) as vulnerabilidades em um sistema. É mais amplo e menos intrusivo.
*   **Penetration Testing (Pentest):** Vai além da identificação; tenta **explorar** a falha para provar o impacto real (conseguir acesso, roubar dados).
    *   *Neste trabalho, o foco é a Análise. A exploração só deve ser feita se autorizada e segura.*

### 1.2 CVE (Common Vulnerabilities and Exposures)
É uma lista pública de falhas de segurança conhecidas. Cada falha recebe um ID único (ex: `CVE-2017-0144` - EternalBlue).
*   **Uso no trabalho:** Ao identificar um serviço desatualizado (ex: Apache 2.4.7), você buscará por "Apache 2.4.7 CVE" para ver quais falhas afetam essa versão.

### 1.3 CVSS (Common Vulnerability Scoring System)
É o padrão para avaliar a **gravidade** de uma vulnerabilidade. A nota vai de 0.0 a 10.0.
*   **Baixa (0.1 - 3.9)**
*   **Média (4.0 - 6.9)**
*   **Alta (7.0 - 8.9)**
*   **Crítica (9.0 - 10.0)**
*   **Uso no trabalho:** Obrigatório para classificar o risco no relatório. Use a [Calculadora CVSS do NVD](https://nvd.nist.gov/vuln-metrics/cvss).

### 1.4 Superfície de Ataque
Representa todos os pontos onde um atacante pode tentar entrar ou extrair dados.
*   **Exemplos:** Portas abertas, serviços rodando, formulários web, APIs expostas.
*   **Objetivo:** Quanto menor a superfície (menos portas abertas), mais seguro.

---

## 2. Tecnologias e Ferramentas

### 2.1 Nmap (Network Mapper)
A principal ferramenta para este trabalho. Usada para descoberta de hosts, varredura de portas e detecção de versões/SO.
*   **NSE (Nmap Scripting Engine):** O "superpoder" do Nmap. Permite rodar scripts (`.nse`) que detectam vulnerabilidades específicas automaticamente.

### 2.2 Scanners de Vulnerabilidade (Opcionais/Complementares)
*   **Nessus / OpenVAS:** Ferramentas automatizadas que geram relatórios bonitos.
    *   *Dica:* Se não puder usar (licença/instalação pesada), o Nmap com scripts (`--script vuln`) substitui bem para fins acadêmicos.

### 2.3 Fontes de Pesquisa (Threat Intelligence)
*   **NVD (National Vulnerability Database):** Banco de dados oficial dos EUA.
*   **Exploit-DB:** Banco de dados de exploits (códigos de ataque).
*   **CVE Details:** Site fácil para buscar históricos de falhas por produto.

---

## 3. Guia Prático de Comandos (Passo a Passo)

Aqui estão os comandos sugeridos para cada etapa do trabalho.

### Etapa 1: Obtenção de Informações (Reconnaissance)
*Objetivo: Identificar o alvo e garantir que está "vivo".*

1.  **Descobrir IP da sua rede:**
    *   Windows: `ipconfig`
    *   Linux: `ip addr` ou `ifconfig`
2.  **Verificar conectividade:**
    *   `ping <IP_ALVO>`
3.  **Identificar rota (se for remoto):**
    *   `tracert <IP_ALVO>` (Windows)
    *   `traceroute <IP_ALVO>` (Linux)
4.  **Varredura de Descoberta (Ping Scan):**
    *   Descobrir quais máquinas estão ligadas na rede `192.168.1.0/24`:
    *   `nmap -sn 192.168.1.0/24`

### Etapa 2: Mapeamento e Identificação (Scanning)
*Objetivo: Encontrar portas abertas, serviços e versões.*

1.  **Scan de Portas (Rápido e Silencioso - SYN Scan):**
    *   `nmap -sS <IP_ALVO>`
    *   *Nota:* Requer privilégios de administrador/root.
2.  **Scan Completo (Todas as portas TCP):**
    *   `nmap -p- <IP_ALVO>`
3.  **Detecção de Versão e Sistema Operacional (Essencial):**
    *   `nmap -sV -O <IP_ALVO>`
    *   `-sV`: Tenta determinar a versão do serviço (ex: OpenSSH 7.2).
    *   `-O`: Tenta adivinhar o SO (ex: Linux Kernel 4.4).
4.  **Scan Agressivo (Tudo em um):**
    *   `nmap -A <IP_ALVO>`
    *   *Cuidado:* Gera muito tráfego e barulho. Roda detecção de OS, versão, traceroute e scripts padrão.

### Etapa 3: Detecção de Vulnerabilidades (Vulnerability Scanning)
*Objetivo: Encontrar as falhas para o relatório.*

1.  **Usando Scripts de Vulnerabilidade do Nmap:**
    *   Este comando roda uma bateria de scripts que checam por CVEs conhecidas nos serviços encontrados:
    *   `nmap --script vuln <IP_ALVO>`
2.  **Scan Específico (Ex: SMB/WannaCry):**
    *   `nmap -p 445 --script smb-vuln-ms17-010 <IP_ALVO>`

---

## 4. Como Elaborar o Relatório (Exemplo Prático)

Ao preencher a **Tabela de Vulnerabilidades** na Etapa 2 do relatório, siga este modelo:

**Cenário Hipotético:** O Nmap detectou `vsftpd 2.3.4` na porta 21.

1.  **Pesquisa:** Vá ao Google e digite `vsftpd 2.3.4 vulnerability` ou `vsftpd 2.3.4 CVE`.
2.  **Achado:** Você encontrará que essa versão tem um "Backdoor Command Execution" (CVE-2011-2523).
3.  **Preenchimento da Tabela:**

| Serviço | Descrição da Falha | Severidade (CVSS) | Referência |
| :--- | :--- | :--- | :--- |
| **FTP (Porta 21)** | O serviço `vsftpd 2.3.4` contém um backdoor malicioso que permite execução remota de código (RCE) se o usuário enviar um rosto feliz `:)` no login. | **Crítica (9.8)** | CVE-2011-2523 |

4.  **Proposta de Correção (Etapa 3):**
    *   "Atualizar imediatamente o serviço vsftpd para a versão mais recente (3.0.x) ou remover o serviço se não for essencial."

---

## 5. Dicas para os Alvos

*   **Alvo 1 (Rede Doméstica):**
    *   Escaneie seu **Roteador Wi-Fi**. Muitas vezes eles têm portas 80 (HTTP) ou 23 (Telnet) abertas com firmwares antigos.
    *   Escaneie uma **Smart TV** ou dispositivo **IoT**. Eles costumam ser muito vulneráveis.
*   **Alvo 2 (Laboratório):**
    *   Escaneie as máquinas vizinhas (com permissão do professor).
    *   Procure por máquinas Windows com compartilhamento de arquivos (SMB) ativo.

> **⚠️ AVISO LEGAL:** Realize varreduras APENAS em equipamentos que você possui ou tem permissão explícita para testar. Escanear redes de terceiros sem autorização pode ser considerado crime.
