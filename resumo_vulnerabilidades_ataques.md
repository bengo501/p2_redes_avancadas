# Resumo Detalhado: Vulnerabilidades e Ataques em Redes

## 1. Obtenção de Informações (Reconnaissance)

O primeiro passo de um ataque é coletar dados sobre o alvo sem ser detectado.

### 1.1 Técnicas Principais

*   **Engenharia Social:** Manipulação psicológica para induzir pessoas a revelar informações confidenciais ou realizar ações inseguras (ex: telefonemas, e-mails falsos).
*   **Phishing:** Mensagens fraudulentas que parecem legítimas para "pescar" dados (senhas, cartões) ou induzir instalação de malware.
*   **Malware:** Software malicioso genérico.
    *   **Vírus:** Anexa-se a arquivos legítimos.
    *   **Spyware:** Monitora atividades secretamente.
    *   **Trojan:** Disfarça-se de programa legítimo.
    *   **Botnets:** Redes de dispositivos zumbis controlados remotamente.
    *   **Ransomware:** Criptografa dados e exige resgate.
*   **Sniffer:** Ferramenta que captura e analisa tráfego de rede (ex: Wireshark, tcpdump).
*   **Port Scan:** Varredura para descobrir portas abertas (serviços ativos) em um host.
    *   *SYN-ACK* = Porta Aberta.
    *   *RST* = Porta Fechada.
    *   *Sem resposta/ICMP filtrado* = Porta Filtrada (Firewall).

### 1.2 Ataque de Dicionário (Quebra de Senhas)
*   **Alvo:** Arquivos de hash de senhas (ex: `/etc/passwd` ou `/etc/shadow`).
*   **Método:** O atacante usa um dicionário de palavras comuns e aplica o mesmo algoritmo de hash usado pelo sistema para tentar encontrar uma correspondência.
*   **Causa:** Usuários criam senhas fracas e previsíveis.
*   **Prevenção:** Políticas de senhas fortes (letras, números, símbolos, sem palavras de dicionário).

---

## 2. Exploração de Protocolos

Muitos protocolos (TCP/IP) foram projetados sem foco em segurança, permitindo diversas explorações.

### 2.1 Spoofing (Falsificação de Identidade)

Técnica onde o atacante se passa por outro host confiável.

*   **ARP Spoofing:** Envia respostas ARP falsas para associar o MAC do atacante ao IP de um gateway ou vítima (permite Man-in-the-Middle).
*   **IP Spoofing:** Falsifica o IP de origem no cabeçalho do pacote. Usado para ocultar identidade ou em ataques de negação de serviço.
    *   *Defesa:* Firewalls que bloqueiem conexões externas baseadas apenas em IP; uso de criptografia/autenticação forte.
*   **DNS Spoofing / Poisoning:** Envia respostas DNS falsas para redirecionar a vítima a sites maliciosos. O *Poisoning* contamina o cache do servidor DNS, afetando todos os seus usuários.
*   **DHCP Spoofing:** Atacante sobe um servidor DHCP falso (Rogue DHCP).
    *   *Ataque:* Responde mais rápido que o servidor legítimo.
    *   *Impacto:* Entrega à vítima um IP válido, mas define o **Gateway Padrão** e o **DNS** como sendo a máquina do atacante (Man-in-the-Middle).

### 2.2 Negação de Serviço (DoS - Denial of Service)

Objetivo: Impedir o uso legítimo de um sistema ou rede, esgotando seus recursos (processamento, memória, banda).

#### **Tipos de DoS:**
*   **TCP SYN Flooding:** Envia milhares de pedidos de conexão (SYN) sem completar o handshake (ACK), lotando a tabela de conexões do servidor.
*   **UDP Flooding:** Inundação de pacotes UDP.
*   **ICMP Flooding:** Inundação de pings.
*   **DHCP Starvation:** Esgota todos os IPs disponíveis no pool do servidor DHCP legítimo usando MACs falsos. Impede novos usuários de entrarem na rede.

### 2.3 Negação de Serviço Distribuído (DDoS)

Usa múltiplos computadores (Botnet) para atacar um único alvo, amplificando o efeito.

*   **Smurf Attack:**
    *   Atacante envia Ping (ICMP Echo) para o endereço de *broadcast* da rede.
    *   IP de origem é falsificado para ser o da **vítima**.
    *   Todas as máquinas da rede respondem à vítima, derrubando-a.
*   **Fraggle Attack:** Similar ao Smurf, mas usa UDP (porta 7/19) em vez de ICMP.

#### **Exemplos Reais de DDoS:**
*   **GitHub (2018):** 1.35 Tbps. Uso de servidores Memcached (UDP) para amplificação (pedidos pequenos geram respostas gigantes).
*   **Cloudflare (2025):** 22.2 Tbps (recorde teórico mencionado). Origem em botnets IoT.

---

## 3. Outras Técnicas de Ataque

### 3.1 Fragmentação
*   Se um pacote é maior que o MTU, ele é fragmentado.
*   **Ataque:** Sobrescrever cabeçalhos durante a remontagem para driblar regras de firewall ou causar instabilidade.
*   **Teardrop / Ping of Death:** Envia fragmentos sobrepostos ou pacotes maiores que o permitido (65.535 bytes), causando *buffer overflow* e travamento do sistema na remontagem.

### 3.2 Man-in-the-Middle (MitM)
*   O atacante intercepta a comunicação entre duas partes sem que elas saibam, podendo ler ou alterar os dados.
*   Facilitado por ARP Spoofing ou DHCP Spoofing.

### 3.3 Ataques via ICMP
*   **ICMP Redirect:** Engana a vítima para usar uma rota maliciosa.
*   **Destination Unreachable:** Forja erro para derrubar conexões ativas.
*   **Ping of Death:** (Citado acima em fragmentação).
