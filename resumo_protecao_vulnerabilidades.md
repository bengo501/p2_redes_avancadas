# Resumo Detalhado: Descobrindo Vulnerabilidades e Mecanismos de Proteção

## 1. Descobrindo Vulnerabilidades

O processo de identificar fraquezas em sistemas e redes envolve diversas técnicas e ferramentas.

### 1.1 Técnicas de Descoberta
*   **Varredura de Portas (Port Scanning):** Uso de ferramentas como **Nmap** para identificar portas abertas e serviços ativos.
*   **Fingerprinting:** Identificação da versão do sistema operacional e serviços rodando no alvo (ex: `nmap -O`).
*   **Sniffing de Tráfego:** Captura de pacotes (Wireshark, tcpdump) para encontrar dados sensíveis ou protocolos inseguros (texto claro).
*   **Testes de Penetração (Pentest):** Simulação autorizada de ataques para explorar falhas (Metasploit, Burp Suite).
*   **Fuzzing:** Envio de dados aleatórios/malformados para tentar causar falhas (ex: buffer overflow) em aplicações.

### 1.2 Scanners de Vulnerabilidades
Ferramentas automatizadas que inspecionam sistemas em busca de falhas conhecidas (CVEs), configurações incorretas e versões desatualizadas.
*   **Exemplos:** OpenVAS, Nessus.
*   **Saída:** Relatórios detalhados com as vulnerabilidades encontradas e sugestões de correção.

---

## 2. Mecanismos de Proteção

As principais defesas contra ataques incluem Firewalls, VPNs, IDS/IPS, Honeypots e Criptografia.

### 2.1 Firewalls
Dispositivo que analisa o tráfego entre redes (ex: Internet e Rede Interna) para aplicar políticas de segurança.
*   **O que faz:** Reforça políticas, registra atividades, limita exposição.
*   **O que NÃO faz:** Não protege contra ataques internos, conexões que não passam por ele (ex: modem 4G no PC), novas vulnerabilidades (0-day) ou vírus em arquivos permitidos.

#### **Tipos de Firewall:**
1.  **Filtro de Pacotes (Stateless):**
    *   Analisa apenas cabeçalhos (IP origem/destino, Portas, Protocolo).
    *   Baseado em ACLs (Listas de Controle de Acesso).
    *   *Vantagens:* Rápido, barato, transparente.
    *   *Desvantagens:* Difícil gerenciar regras complexas, vulnerável a IP Spoofing, não entende o estado da conexão.
    *   *Políticas:* "Permissiva" (tudo liberado, bloqueia o proibido) vs "Restritiva" (tudo bloqueado, libera o permitido - **Recomendada**).

2.  **Stateful Firewall:**
    *   Monitora o **estado** das conexões.
    *   Mantém uma tabela de estados (IPs, portas, número de sequência).
    *   **Regra Implícita:** Se uma conexão sai da rede interna, a resposta é automaticamente permitida.

3.  **Firewall de Aplicação (Proxy):**
    *   Intermedeia a conexão: Cliente <-> Proxy <-> Servidor.
    *   Analisa o conteúdo da aplicação (L7).
    *   *Vantagens:* Controle detalhado, cache, autenticação de usuários, esconde a rede interna.
    *   *Desvantagens:* Mais lento, exige configuração específica para cada serviço.

4.  **NGFW (Next-Generation Firewall):**
    *   Combina firewall tradicional + IPS + Controle de Aplicação + Antivírus + Integração com identidade (AD/LDAP).

#### **Arquiteturas de Firewall:**
*   **DMZ (Demilitarized Zone):** Rede de perímetro isolada (física ou logicamente) que contém serviços públicos (Web, Email). Protege a rede interna caso um servidor público seja comprometido.
*   **Firewall de Estação (Host-based):** Software no próprio SO (ex: Windows Firewall) para defesa em profundidade.

---

### 2.2 VPN (Virtual Private Network)
Rede privada construída sobre uma rede pública (Internet) usando **tunelamento** e **criptografia**.
*   **Benefícios:** Confidencialidade, Integridade, Autenticação, Anonimato (mascara IP real).
*   **Protocolos:**
    *   *PPTP / L2F:* Obsoletos e inseguros.
    *   *L2TP/IPSec:* Padrão industrial, seguro (IPSec provê a criptografia).
    *   *IPSec:* Suíte completa de segurança (Autenticação, Criptografia, Integridade). Obrigatório no IPv6.
    *   *OpenVPN:* Popular, open-source, usa SSL/TLS (TCP/UDP).
    *   *WireGuard:* Moderno, leve, rápido, criptografia de ponta (ChaCha20).
*   **Tipos:** Acesso Remoto (usuário <-> empresa), Site-to-Site (matriz <-> filial), Pessoal (usuário <-> internet segura).

---

### 2.3 IDS e IPS

#### **IDS (Intrusion Detection System)**
*   **Função:** Detecta e alerta sobre atividades suspeitas (passivo).
*   **Tipos de Detecção:**
    *   *Assinatura:* Compara com padrões conhecidos (Snort). Eficaz para ataques conhecidos, cego para novos.
    *   *Anomalia:* Aprende o comportamento "normal" e alerta desvios. Pode gerar muitos falsos positivos.
*   **Escopo:**
    *   *NIDS (Network):* Monitora tráfego da rede em pontos estratégicos.
    *   *HIDS (Host):* Monitora logs e integridade de arquivos em um host específico (ex: OSSEC).

#### **IPS (Intrusion Prevention System)**
*   **Função:** Detecta e **bloqueia** ataques (ativo).
*   **Ação:** Derruba pacotes, reconfigura firewall, encerra conexões TCP.

---

### 2.4 Honeypots
Sistemas "isca" com vulnerabilidades propositais e dados falsos para atrair atacantes.
*   **Objetivo:** Desviar ataques de sistemas reais e estudar o comportamento do invasor.

---

## 3. Criptografia e Autenticação

### 3.1 Criptografia Simétrica (Chave Única)
*   Mesma chave para cifrar e decifrar.
*   **Algoritmos:**
    *   *AES:* Padrão atual, seguro (128/256 bits).
    *   *DES/3DES:* Obsoletos.
    *   *ChaCha20:* Moderno, rápido (alternativa ao AES).
    *   *RC4:* Obsoleto e inseguro.
*   **Prós:** Rápido. **Contras:** Dificuldade na troca segura da chave (key distribution problem).

### 3.2 Criptografia Assimétrica (Chave Pública)
*   Par de chaves: **Pública** (cifra) e **Privada** (decifra).
*   **Algoritmos:**
    *   *RSA:* Mais famoso, usado para cifragem e assinatura.
    *   *Diffie-Hellman (DH) / ECDH:* Usados apenas para **troca de chaves** segura.
*   **Prós:** Resolve o problema da troca de chaves, garante autenticidade e não-repúdio. **Contras:** Lento.

### 3.3 Assinatura Digital
*   Garante **Autenticidade**, **Integridade** e **Não-Repúdio**.
*   **Processo Inverso:** Assina com a **Chave Privada** (emissor) e verifica com a **Chave Pública** (receptor).
*   **Hash:** Para eficiência, assina-se o *hash* do documento, não o documento inteiro.
*   **Algoritmos:** RSA, DSA, ECDSA (Curvas Elípticas - Bitcoin/Ethereum).
