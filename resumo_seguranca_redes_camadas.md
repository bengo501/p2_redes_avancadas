# Resumo Detalhado: Segurança em Redes de Computadores

## 1. Conceitos Iniciais

### 1.1 Pilha TCP/IP: Abordagem Bottom-Up
A segurança em redes é analisada camada por camada, da física até a aplicação, identificando vulnerabilidades, métodos de detecção e mitigação em cada nível.

---

## 2. Filtragem de Pacotes e Firewalls

A filtragem de pacotes é o processo de decidir o destino de um pacote (permitir, negar, rejeitar, registrar, etc.) com base em critérios pré-definidos.

### 2.1 Tipos de Filtragem e Firewalls

*   **Packet Filter (Stateless ACL):**
    *   Decide por pacote individualmente.
    *   Não mantém estado da conexão.
    *   Baseia-se em: IP origem/destino, protocolo, portas, tipo ICMP.
    *   Exemplo: ACLs de roteadores.

*   **Stateful Firewall:**
    *   Mantém uma tabela de estados das conexões (ex: TCP handshake).
    *   Rejeita pacotes que não pertencem a uma sessão válida.
    *   Estados: NEW, ESTABLISHED, RELATED.

*   **Application Proxy / Reverse Proxy (L7):**
    *   Atua na camada de aplicação, intermediando conexões.

*   **WAF (Web Application Firewall):**
    *   Proteção específica para aplicações web (HTTP/HTTPS).
    *   Usa regras (ex: OWASP CRS) e assinaturas contra ataques como SQL Injection e XSS.

*   **NGFW (Next-Gen Firewalls):**
    *   Combina firewall stateful + DPI (Deep Packet Inspection) + Identificação de Aplicação (App-ID) + Integração com Threat Intelligence/IDS.

*   **Microsegmentation / Distributed Firewall:**
    *   Políticas aplicadas no nível do hypervisor, permitindo controle de tráfego "leste-oeste" (entre servidores) sem passar por roteador físico.

*   **Cloud-Native Firewalls:**
    *   Exemplos: Security Groups (stateful) e Network ACLs (stateless) na AWS.

### 2.2 Problemas Comuns
*   Movimentação lateral de atacantes.
*   Manutenção de IOCs (Indicators of Compromise) atualizados.
*   Ranges de IP com múltiplos serviços misturados.

---

## 3. Sistemas de Detecção de Intrusão (IDS/IPS)

*   **IDS (Intrusion Detection System):** Apenas detecta e alerta. (HIDS = Host-based, NIDS = Network-based).
*   **IPS (Intrusion Prevention System):** Detecta e bloqueia ativamente. (HIPS, NIPS).

### 3.1 Métodos de Detecção
*   **Assinatura:** Compara com padrões conhecidos de ataques.
*   **Heurística / Anomalia:** Identifica desvios do comportamento normal.
*   **Stateful Packet Analysis:** Analisa o contexto da conexão.
*   **Machine Learning / Behavioral:** Aprende o padrão normal e detecta desvios complexos.

*   **Exemplos:** Snort, Zeek, OSSEC/Wazuh.

---

## 4. Segurança por Camadas (Layer by Layer)

### 4.1 Camada 1 - Física (L1)

*   **Vulnerabilidades:**
    *   **Eavesdropping/Sniffing:** Escuta passiva (acesso físico, tapping em cabos).
    *   **Jamming (Interferência):**
        *   *Continuous:* Sinal contínuo ocupando o canal.
        *   *Deceptive:* Envio de pacotes falsos.
        *   *Reactive:* Transmite apenas quando detecta sinal legítimo (difícil detecção).
    *   **Wi-Fi (802.11):** Banda 2.4GHz congestionada; DSSS e OFDM suscetíveis a interferência.
    *   **Bluetooth/Zigbee:** Afetados por ruído de banda larga.

*   **Detecção:**
    *   Monitoramento SNMP (traps de link up/down, erros CRC).
    *   NetFlow (ausência súbita de tráfego).
    *   Análise de espectro (Spectrum Analyzer).

*   **Mitigação:**
    *   Controle de acesso físico (CCTV, portas trancadas).
    *   Cabos blindados e redundância.
    *   **Expansão Espectral (Spread Spectrum):** DSSS e OFDM dificultam interceptação e interferência.
    *   Gaiola de Faraday.

### 4.2 Camada 2 - Enlace (L2)

*   **Vulnerabilidades:**
    *   **ARP Spoofing:** Falsificação de respostas ARP para Man-in-the-Middle.
    *   **CAM Table Flooding:** Inundar tabela MAC do switch para forçar modo "fail-open" (hub).
    *   **VLAN Hopping:** Acesso indevido a VLANs via manipulação de tags ou DTP.
    *   **Manipulação de STP:** Forçar mudança de Root Bridge.
    *   **DHCP Starvation/Rogue DHCP:** Esgotar IPs e subir servidor DHCP falso.

*   **Detecção:**
    *   Ferramentas: `arpwatch`, `tcpdump`.
    *   SNMP: Monitorar tabela de MACs (`dot1dTpFdbTable`).
    *   Logs do switch.

*   **Mitigação:**
    *   **Dynamic ARP Inspection (DAI):** Valida ARP contra tabela confiável.
    *   **Port Security:** Limita MACs por porta.
    *   **BPDU Guard:** Protege topologia STP.
    *   **802.1X (NAC):** Autenticação de dispositivos.
    *   Desabilitar negociação automática de trunk (DTP).

### 4.3 Camada 3 - Rede / IP (L3)

*   **Vulnerabilidades:**
    *   **IP Spoofing:** Falsificação de IP de origem (usado em DDoS).
    *   **Abuso de ICMP:** Smurf attack, Ping Floods.
    *   **Ataques de Fragmentação:** Teardrop (bugs na remontagem de pacotes).
    *   **Roteamento:** Sequestro de prefixos BGP (Hijacks).

*   **Detecção:**
    *   NetFlow (análise de volume e padrões de tráfego).
    *   IDS (detecção de pacotes anômalos, TTLs inconsistentes).
    *   Monitoramento BGP (RPKI).

*   **Mitigação:**
    *   **uRPF (Unicast Reverse Path Forwarding):** Verifica se a origem é roteável pela interface de entrada.
    *   **Egress Filtering (BCP38):** Bloqueia saída de pacotes com IP spoofado da sua rede.
    *   **Segurança BGP:** Filtros de prefixo e RPKI.

### 4.4 Camada 4 - Transporte (L4)

*   **Vulnerabilidades:**
    *   **SYN Flood:** Esgotamento da tabela de conexões com pacotes SYN sem ACK.
    *   **Amplificação UDP:** Uso de serviços (DNS, NTP) para refletir e amplificar tráfego para a vítima.

*   **Detecção:**
    *   NetFlow (alta taxa de SYN sem ACK, razão bytes/packets alta em UDP).
    *   SNMP (monitorar conexões ativas).
    *   Métricas do Kernel (`netstat`, `ss`).

*   **Mitigação:**
    *   **SYN Cookies:** Responde a SYNs sem alocar estado inicial.
    *   **Rate Limiting:** Limitar taxa de tráfego.
    *   **Connection Limiting:** Limitar conexões por IP.
    *   Fechar amplificadores abertos (configuração correta de DNS/NTP).

### 4.5 Camada 7 - Aplicação (L7)

*   **Vulnerabilidades:**
    *   **Injeção:** SQLi, Command Injection, XSS.
    *   **Abuso de Protocolo:** DNS Cache Poisoning.
    *   **Exfiltração Cifrada:** Uso de HTTPS para roubar dados.

*   **Detecção:**
    *   NetFlow (anomalias de exfiltração).
    *   Logs de WAF/Proxy (padrões de URI suspeitos, erros 4xx/5xx).
    *   Zeek (análise de metadados TLS/HTTP).

*   **Mitigação:**
    *   **WAF:** Regras robustas (OWASP CRS).
    *   **Hardening de TLS:** TLS 1.2/1.3, HSTS.
    *   **Desenvolvimento Seguro:** Prepared statements (contra SQLi), validação de entrada.

---

## 5. Análise de Vulnerabilidades

Processo geralmente automatizado para identificar fraquezas.

*   **Etapas:**
    1.  Identificação (Discovery).
    2.  Validação e Classificação.
    3.  Avaliação de Risco e Priorização.
    4.  Planejamento da Remediação.
    5.  Remediação e Verificação (ex: virtual patching).
    6.  Monitoramento Contínuo.

*   **Conceitos Chave:** CVE (Identificador), CVSS (Score de risco), NVD (Base de dados).
