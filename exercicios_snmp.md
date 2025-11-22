# Exercícios de Gerência de Redes – SNMP

---

## 1) Dispositivo escolhido e 10 informações gerenciáveis

**Dispositivo:** *Router Cisco ISR 4321* (router de borda típico, usado em escritórios de médio porte).  

| # | Informação (nome) | Tipo de retorno | Tipo de acesso | Área funcional (FCAPS) | Descrição do retorno |
|---|-------------------|----------------|----------------|------------------------|----------------------|
| 1 | **sysDescr** | *String* (até 255 caracteres) | **Read‑Only** | **F – Fault Management** (identificação) | Texto que descreve o hardware, versão do IOS, modelo e número de série. Ex.: `Cisco IOS Software, ISR Software (X86_64_LINUX_IOSD-UNIVERSALK9-M), Version 16.9.3, RELEASE SOFTWARE (fc2)` |
| 2 | **sysUpTime** | *TimeTicks* (centésimos de segundo) | **Read‑Only** | **F – Fault Management** (tempo de operação) | Tempo decorrido desde a última reinicialização do router. Ex.: `12345678` (≈ 34 h 12 min). |
| 3 | **sysContact** | *String* | **Read‑Write** | **C – Configuration Management** | Nome e e‑mail do responsável pelo equipamento. Ex.: `John Doe <john.doe@example.com>` |
| 4 | **ifDescr** (interface GigabitEthernet0/0/0) | *String* | **Read‑Only** | **F – Fault Management** | Descrição textual da interface, normalmente o nome da porta. Ex.: `GigabitEthernet0/0/0` |
| 5 | **ifOperStatus** (GigabitEthernet0/0/0) | *INTEGER* (1=up, 2=down, 3=testing) | **Read‑Only** | **F – Fault Management** | Estado operacional atual da interface. Ex.: `1` (up). |
| 6 | **ifInOctets** (GigabitEthernet0/0/0) | *Counter64* | **Read‑Only** | **P – Performance Management** | Total de octetos recebidos pela interface desde o último reset. Ex.: `9876543210`. |
| 7 | **ifOutOctets** (GigabitEthernet0/0/0) | *Counter64* | **Read‑Only** | **P – Performance Management** | Total de octetos enviados pela interface. |
| 8 | **ipForwarding** | *INTEGER* (1=forwarding enabled, 2=disabled) | **Read‑Write** | **C – Configuration Management** | Indica se o router está atuando como roteador IP (forwarding). |
| 9 | **tcpCurrEstab** | *INTEGER* | **Read‑Only** | **P – Performance Management** | Número atual de conexões TCP estabelecidas. |
|10| **udpInDatagrams** | *Counter32* | **Read‑Only** | **P – Performance Management** | Contador de datagramas UDP recebidos com sucesso. |

**Resultado:** Cada uma dessas informações pode ser consultada via **OID** correspondente (ex.: `1.3.6.1.2.1.1.1.0` para *sysDescr*) ou modificada quando o *tipo de acesso* permite escrita.  

---

## 2) Análise dos objetos da MIB‑II e suas áreas funcionais

> **FCAPS** – modelo clássico de gerenciamento de redes:  
> **F** – Fault Management  
> **C** – Configuration Management  
> **A** – Accounting Management  
> **P** – Performance Management  
> **S** – Security Management

### 2.1 System

| Objeto | Tipo | Área(s) funcional(is) | Comentário (RFC 1213) |
|--------|------|-----------------------|-----------------------|
| **sysDescr** | String | F, C (identificação do equipamento) | Texto livre que descreve hardware, versão do SO e firmware. |
| **sysUpTime** | TimeTicks | F, P (tempo de disponibilidade) | Tempo desde a última reinicialização – usado para cálculo de disponibilidade. |
| **sysContact** | String | C, S (informação de contato para incidentes) | Nome e e‑mail do responsável; útil para notificação de falhas. |

### 2.2 IP

| Objeto | Tipo | Área(s) funcional(is) | Comentário |
|--------|------|-----------------------|-----------|
| **ipForwarding** | INTEGER (1/2) | C (configuração de roteamento) | Habilita ou desabilita o encaminhamento de datagramas IP. |
| **ipInHdrErrors** | Counter32 | F (detecção de falhas) | Contador de datagramas descartados por erro de cabeçalho – indica problemas de integridade. |
| **ipInAddrErrors** | Counter32 | F (detecção de falhas) | Contador de datagramas descartados por erro de endereço – útil para detectar spoofing ou rotas incorretas. |
| **ipReasmOKs** | Counter32 | P (performance de fragmentação) | Número de datagramas IP fragmentados que foram remontados com sucesso. |
| **ipRouteDest** | IpAddress | C (configuração de rotas) | Endereço de destino da rota – parte da tabela de roteamento. |

### 2.3 TCP

| Objeto | Tipo | Área(s) funcional(is) | Comentário |
|--------|------|-----------------------|-----------|
| **tcpMaxConn** | INTEGER | C (limite de recursos) | Número máximo de conexões TCP simultâneas que o dispositivo aceita. |
| **tcpInSegs** | Counter64 | P (volume de tráfego) | Total de segmentos TCP recebidos (incluindo com erro). |
| **tcpConnRemAddress** | IpAddress | F / P (diagnóstico de conexão) | Endereço IP remoto da conexão TCP – usado para rastrear sessões problemáticas. |
| **tcpInErrs** | Counter32 | F (detecção de falhas) | Segmentos TCP descartados por erros (checksum, etc.). |
| **tcpRetransSegs** | Counter32 | P (performance) | Número de segmentos retransmitidos – indica perda de pacotes ou congestionamento. |

### 2.4 UDP

| Objeto | Tipo | Área(s) funcional(is) | Comentário |
|--------|------|-----------------------|-----------|
| **udpInDatagrams** | Counter32 | P (volume de tráfego) | Total de datagramas UDP entregues aos processos locais. |
| **udpNoPorts** | Counter32 | F (detecção de falhas) | Datagramas recebidos em portas sem aplicação – pode indicar varredura ou tráfego indesejado. |
| **udpInErrors** | Counter32 | F (detecção de falhas) | Datagramas UDP que não puderam ser entregues por motivos diferentes de porta inexistente (ex.: checksum). |
| **udpOutDatagrams** | Counter32 | P (volume de tráfego) | Total de datagramas UDP enviados pelo dispositivo. |

### 2.5 Interfaces

| Objeto | Tipo | Área(s) funcional(is) | Comentário |
|--------|------|-----------------------|-----------|
| **ifDescr** | String | F (identificação da interface) | Descrição textual da interface (ex.: `GigabitEthernet0/1`). |
| **ifType** | INTEGER | F (classificação) | Tipo da interface (ex.: 6 = Ethernet, 24 = Loopback). |
| **ifMtu** | INTEGER | P (performance) | MTU máximo suportado – influencia a fragmentação de pacotes. |
| **ifAdminStatus** | INTEGER (1=up, 2=down, 3=testing) | C (controle administrativo) | Estado administrativo da interface – pode ser alterado via *Set*. |
| **ifInUcastPkts** | Counter32 | P (volume de tráfego) | Número de pacotes unicast recebidos – métrica de carga da interface. |

---

## 3) Como usar essas informações na prática

1. **Coleta via SNMP GET/GETBULK** – Para obter rapidamente contadores de desempenho (ex.: `ifInOctets`, `tcpRetransSegs`) use **GetBulkRequest**.  
2. **Monitoramento de falhas** – Configure **traps** ou **informRequests** para objetos de *fault* como `ipInHdrErrors` ou `udpNoPorts`.  
3. **Ajuste de configuração** – Modifique objetos *read‑write* (`sysContact`, `ipForwarding`, `ifAdminStatus`) com **SET** quando precisar habilitar/desabilitar funcionalidades.  
4. **Relatórios de disponibilidade** – Combine `sysUpTime` com contadores de falhas para gerar métricas de **Uptime** e **MTBF** (Mean Time Between Failures).  
5. **Contabilidade (Accounting)** – Embora a MIB‑II não possua objetos específicos de *accounting*, os contadores de tráfego (`ifInOctets`, `udpOutDatagrams`) podem ser usados para estimar uso de banda e, consequentemente, custos. 

---

## 4) Resultado esperado ao executar os exercícios

* **Lista de 10 informações** – pronta para ser inserida em um script de coleta (ex.: Python + pysnmp).  
* **Mapa de áreas funcionais** – auxilia na definição de políticas de monitoramento (ex.: quais objetos vão gerar alarmes de *fault* vs. quais serão usados em *performance dashboards*).  
* **Documentação** – o markdown acima serve como base para o **Manual de Gerenciamento SNMP** da sua organização. 

---

*Este arquivo foi gerado como `exercicios_snmp.md` e pode ser salvo em seu workspace para referência futura.*
