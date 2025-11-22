# Exercícios Práticos de Segurança de Redes

> **Aviso Importante:** Estes exercícios envolvem técnicas ofensivas (ataques de rede). Execute-os **APENAS** em um ambiente controlado (laboratório, máquinas virtuais) ou em redes onde você tem permissão explícita. Atacar redes de terceiros sem autorização é crime.

---

## 1. Ataque de Flooding ICMP (Smurf Attack)

**Comando Sugerido:** `sudo ping -b -f 10.32.143.255`

### **Explicação Conceitual**
Este exercício simula um ataque de negação de serviço (DoS) antigo conhecido como **Smurf Attack**.
*   **Broadcast (`-b`):** O comando envia pacotes para o endereço de broadcast da rede (`.255`). Isso significa que o pacote é destinado a *todas* as máquinas daquela sub-rede.
*   **Flood (`-f`):** O modo "flood" envia pacotes o mais rápido possível, sem esperar resposta.
*   **O Ataque:** O atacante envia um ping para o broadcast falsificando o IP de origem (spoofing) para ser o da **vítima**. Todas as máquinas da rede recebem o ping e respondem simultaneamente para a vítima, sobrecarregando-a.

### **Passo a Passo e Resultado Esperado**
1.  Execute o comando em uma rede de laboratório.
2.  **Resultado:** Você verá uma enxurrada de respostas ICMP. Se monitorado com Wireshark, verá milhares de pacotes `Echo Reply` indo para o IP de origem.
3.  **Mitigação:** Roteadores modernos são configurados por padrão para não encaminhar pacotes de broadcast direcionado, e sistemas operacionais modernos (Windows/Linux) geralmente ignoram pings de broadcast.

---

## 2. ARP Spoofing (Man-in-the-Middle)

**Comando:** `arpspoof -i eth0 -t <IP_Alvo> <IP_Gateway>`

### **Explicação Conceitual**
O protocolo ARP (Address Resolution Protocol) mapeia endereços IP para endereços MAC (físicos). Ele não possui autenticação.
*   **O Ataque:** O `arpspoof` envia mensagens ARP falsas ("gratuitous ARP") para a rede.
*   Ele diz ao **Alvo**: "Eu sou o Gateway".
*   Ele diz ao **Gateway**: "Eu sou o Alvo".
*   **Resultado:** Todo o tráfego entre o alvo e a internet passa pela máquina do atacante, permitindo interceptação (sniffing) ou modificação.

### **Passo a Passo**
1.  Instale o dsniff: `sudo apt-get install dsniff`.
2.  Habilite o roteamento de pacotes no atacante (para não derrubar a conexão da vítima):
    `echo 1 > /proc/sys/net/ipv4/ip_forward`
3.  Execute o ataque: `arpspoof -i eth0 -t 192.168.1.50 192.168.1.1`
4.  **Wireshark:** Você verá pacotes ARP repetitivos dizendo "192.168.1.1 is at [MAC_DO_ATACANTE]". Se a vítima navegar na web, você verá o tráfego HTTP dela passando pela sua interface.

---

## 3. Varredura de Portas com Nmap

O Nmap é a ferramenta padrão para reconhecimento de rede.

### **Análise das Opções**

| Comando | Funcionalidade | Análise no Wireshark |
| :--- | :--- | :--- |
| **a) -v** | **Verbose:** Aumenta o detalhamento da saída no terminal. | Não altera o tráfego de rede, apenas a exibição. |
| **b) -sT** | **TCP Connect Scan:** Realiza o handshake completo (SYN, SYN-ACK, ACK). | Você verá conexões TCP completas estabelecidas e depois encerradas (RST/FIN). É mais lento e barulhento nos logs. |
| **c) -sU** | **UDP Scan:** Varre portas UDP (DNS, SNMP, etc.). | Envia pacotes UDP vazios. Se receber "ICMP Port Unreachable", a porta está fechada. Se não receber nada, está "Open/Filtered". |
| **d) -sP** | **Ping Scan:** Verifica apenas se o host está online (não varre portas). | Envia ICMP Echo Request e/ou TCP SYN para porta 443/80. |
| **e) -sS** | **SYN Scan (Stealth):** O padrão. Envia SYN, recebe SYN-ACK, envia RST. | Não completa a conexão ("half-open"). É mais rápido e menos visível em logs de aplicação. |
| **f) -sA** | **ACK Scan:** Usado para mapear regras de firewall. | Envia pacotes com flag ACK. Se receber RST, a porta não está filtrada (unfiltered). Se não responder, está filtrada (stateful firewall). |
| **g) -sW** | **Window Scan:** Similar ao ACK, mas analisa o campo TCP Window. | Tenta determinar portas abertas/fechadas baseada em anomalias de implementação TCP (pouco confiável hoje). |
| **h) -sM** | **Maimon Scan:** Técnica antiga (FIN/ACK). | Geralmente ineficaz em sistemas modernos (BSD-derived). |
| **i) ... --script=vuln** | **Vulnerability Scan:** Usa scripts NSE para detectar falhas conhecidas. | Gera muito tráfego específico de aplicação (ex: tentativas de login, requisições HTTP maliciosas). Muito "barulhento". |
| **j) -O** | **OS Detection:** Tenta adivinhar o Sistema Operacional. | Envia pacotes malformados/estranhos e analisa como a pilha TCP/IP do alvo responde (fingerprinting). |
| **k) --open** | **Show Open Ports:** Mostra apenas portas abertas na saída. | Filtro de exibição, não altera o tráfego. |
| **l) --iflist** | **Interface List:** Lista interfaces de rede e rotas da própria máquina. | Comando local, não gera tráfego de rede. |
| **m) -f** | **Fragment Packets:** Fragmenta os pacotes IP. | Divide o cabeçalho TCP em pequenos fragmentos IP para tentar evadir firewalls/IDS antigos. |

---

## 4. Integridade – Uso de Hash

**Conceito:** Hash é uma "impressão digital" única de um arquivo. Qualquer alteração no conteúdo muda drasticamente o hash.

### **Passo a Passo e Resultados**
1.  **Criar arquivo:** `echo "Teste" > arquivo.txt`
2.  **Hash Original (a):** `md5sum arquivo.txt` -> Ex: `d41d8cd98f00b204e9800998ecf8427e`
3.  **Alterar (b):** `echo "Teste2" > arquivo.txt` -> Hash muda completamente.
4.  **Restaurar (c):** `echo "Teste" > arquivo.txt` -> Hash volta a ser exatamente o original.
5.  **Fatores (d):** O hash depende **apenas do conteúdo (bits)** do arquivo. Data de modificação, permissões ou dono **não** alteram o hash do conteúdo (embora alterem o hash do sistema de arquivos/metadados).
6.  **Nome do Arquivo (e):** Mudar o nome (`mv arquivo.txt novo.txt`) **não altera** o hash `md5sum`. O conteúdo permanece o mesmo.

---

## 5. Chave Pública e Privada (GPG)

**Conceito:** Criptografia Assimétrica.
*   **Confidencialidade:** Criptografo com a **Chave Pública** do destinatário. Só a **Chave Privada** dele abre.
*   **Autenticidade/Assinatura:** Assino com minha **Chave Privada**. Qualquer um com minha **Chave Pública** confirma que fui eu.

### **Passo a Passo**
1.  **Gerar Chaves (a):** `gpg --gen-key`. Cria o par (pub/sec) em `~/.gnupg`.
2.  **Exportar (b):** `gpg --export -a "Seu Nome" > minha_publica.asc`. O flag `-a` cria um arquivo texto (ASCII armored).
3.  **Trocar (c/d):** Envie o arquivo `.asc` para o colega. Ele roda `gpg --import minha_publica.asc`. Agora ele tem sua chave no chaveiro dele.
4.  **Criptografar (e):** O colega roda: `gpg -e -r "Seu Nome" segredo.txt`. Isso gera `segredo.txt.gpg`.
    *   *Conceito:* Ele usou sua chave pública. Só você pode ler isso.
5.  **Descriptografar (g.i):** Você recebe o arquivo e roda: `gpg -d segredo.txt.gpg`. O GPG pede sua senha (passphrase) para desbloquear sua chave privada e decifrar a mensagem.
6.  **Assinar (f):** Você roda: `gpg --clearsign aviso.txt`. Isso cria `aviso.txt.asc` com o texto legível + uma assinatura embaixo.
7.  **Verificar (g.ii):** O colega roda `gpg --verify aviso.txt.asc`. O GPG diz "Good signature from Seu Nome", provando que o texto não foi alterado e veio de você.
