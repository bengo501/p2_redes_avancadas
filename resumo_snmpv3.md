# Resumo Detalhado – SNMPv3

> **Objetivo:** Apresentar, de forma clara e completa, os principais conceitos, arquitetura, módulos, modelos de segurança e controle de acesso definidos na especificação SNMPv3 (RFC 3410‑3418).  

---

## 1. Por que o SNMPv3 foi criado?

| Requisito | Motivo |
|-----------|--------|
| **Reutilização de trabalhos anteriores** | Aproveitar as funcionalidades já consolidadas do SNMPv2 (PDUs, operações, modelo de gerenciamento). |
| **Segurança para mensagens do tipo *set*** | Corrigir a vulnerabilidade da *community string* (texto‑claro) presente no SNMPv1/v2c. |
| **Arquitetura modular** | Permitir que diferentes ambientes (routers, switches, servidores, IoT) implementem apenas os módulos que necessitam, facilitando extensões e a inclusão de novos modelos de segurança. |
| **Manter a simplicidade** | Apesar das novas funcionalidades, o protocolo continua “simple” para quem desenvolve agentes ou gerentes. |

> **Resultado:** SNMPv3 = **SNMPv2 + camada de segurança (USM) + controle de acesso (VACM)**, tudo organizado em módulos bem‑definidos.

---

## 2. Visão geral da arquitetura SNMPv3

```
+-------------------+        +-------------------+
|  SNMP ENGINE      |<----->|  SNMP ENGINE      |
| (Gerente)         |        | (Agente)          |
+-------------------+        +-------------------+
|  Dispatcher       |        |  Dispatcher       |
|  Message Proc.    |        |  Message Proc.    |
|  Security (USM)   |        |  Security (USM)   |
|  Access Control   |        |  Access Control   |
+-------------------+        +-------------------+
|  Applications:    |        |  Applications:    |
|  • Command Gen.   |        |  • Command Resp.  |
|  • Notif. Recv.   |        |  • Notif. Orig.   |
|  • Proxy (opt.)   |        |  • Proxy (opt.)   |
+-------------------+        +-------------------+
```

* Cada **entidade SNMP** (gerente ou agente) pode implementar **qualquer combinação** dos módulos acima.  
* O **Dispatcher** permite que diferentes versões de mensagens (v1, v2c, v3) coexistam na mesma engine.  
* O **Message Processing Subsystem** cuida da codificação/decodificação das PDUs.  
* O **Security Subsystem** (USM) fornece **autenticação** e **privacidade**.  
* O **Access Control Subsystem** (VACM) decide se o usuário tem permissão para ler/escrever determinado objeto.  

---

## 3. Módulos da SNMP Engine

| Módulo | Função principal | Principais responsabilidades |
|--------|------------------|------------------------------|
| **Dispatcher** | Multiplexação de mensagens | - Recebe PDUs de diferentes versões;<br>- Encaminha para o subsistema adequado. |
| **Message Processing Subsystem** | Preparação e extração de mensagens | - Monta a mensagem SNMP (header + PDU) antes do envio;<br>- Desempacota a mensagem recebida, validando tamanho e formato. |
| **Security Subsystem (USM)** | Autenticação & Criptografia | - Calcula/ verifica HMAC (MD5/SHA‑1/…);<br>- Criptografa payload (DES, AES, …);<br>- Gerencia chaves e parâmetros de segurança. |
| **Access Control Subsystem (VACM)** | Controle de acesso baseado em visão | - Avalia tabelas de usuários, grupos, vistas e permissões;<br>- Determina se a operação (GET, SET, …) é permitida. |

---

## 4. Aplicações (funções de alto nível)

| Aplicação | Onde está implementada | Descrição |
|-----------|-----------------------|-----------|
| **Command Generator** | Gerente | Cria PDUs **Get**, **GetNext**, **GetBulk**, **Set** e envia ao agente; processa a resposta. |
| **Command Responder** | Agente | Recebe PDUs de comando, verifica acesso via VACM, executa a operação e devolve **GetResponse**. |
| **Notification Originator** | Agente | Monitora eventos (ex.: linkDown) e gera **Trap** ou **InformRequest**. |
| **Notification Receiver** | Gerente | Escuta por **Trap/Inform**; responde a **Inform** com **Response‑PDU**. |
| **Proxy Forwarder** *(opcional)* | Ambos | Reencaminha mensagens entre diferentes domínios de gerenciamento (ex.: entre redes com diferentes versões ou políticas). |

---

## 5. Gerente × Agente em SNMPv3

| Papel | Módulos obrigatórios | Módulos opcionais |
|-------|----------------------|-------------------|
| **Gerente** | Dispatcher, Message Proc., Security, Access Control, Command Generator, Notification Receiver | Proxy Forwarder |
| **Agente** | Dispatcher, Message Proc., Security, Access Control, Command Responder, Notification Originator | Proxy Forwarder |

> **Flexibilidade:** Uma mesma entidade pode atuar simultaneamente como gerente **e** agente (ex.: um roteador que gerencia um módulo interno e, ao mesmo tempo, aceita gerenciamento externo).  

---

## 6. Modelo de Segurança do Usuário (USM)

### 6.1 Níveis de segurança

| Nível | Significado | Quando usar |
|-------|--------------|-------------|
| **noAuthNoPriv** | Mensagem sem autenticação nem criptografia. | Compatibilidade com dispositivos legados que não suportam segurança. |
| **authNoPriv** | Autenticação (HMAC) **sem** criptografia. | Quando a integridade é suficiente, mas a confidencialidade não é crítica. |
| **authPriv** | Autenticação **e** criptografia (confidencialidade). | Ambiente sensível – dados de gerenciamento não podem ser lidos ou alterados por terceiros. |

### 6.2 Componentes da mensagem USM

| Campo | Descrição |
|-------|-----------|
| **msgVersion** | Sempre “3”. |
| **msgID** | Identificador único da mensagem (correlação request/response). |
| **msgMaxSize** | Tamanho máximo, em octetos, que o emissor aceita receber. |
| **msgFlags** (3 bits) | - **authFlag** (bit 0): 1 → autenticação presente.<br>- **privFlag** (bit 1): 1 → criptografia presente.<br>- **reportableFlag** (bit 2): 1 → envia **Report PDU** em caso de erro (ex.: falha de descriptografia). |
| **msgSecurityModel** | 1 → SNMPv1, 2 → SNMPv2c, 3 → USM (default). |
| **msgSecurityParameters** | Estrutura que contém: <br>• **engineID** (identificador da SNMP Engine);<br>• **engineBoots** e **engineTime** (para evitar replay attacks);<br>• **userName**; <br>• **authParameters** (HMAC); <br>• **privParameters** (IV, salt, …). |
| **contextEngineID** | Identifica a engine que contém o contexto (geralmente o mesmo do emissor). |
| **contextName** | Nome lógico que delimita um “sub‑conjunto” da MIB (ex.: *card1*, *card2*). |
| **PDU** | Formato idêntico ao SNMPv2 (Get, GetNext, GetBulk, Set, Inform, Report, …). |

### 6.3 Ameaças mitigadas pelo USM

| Ameaça | Como o USM protege |
|--------|--------------------|
| **Modificação de informação** | HMAC garante integridade; o receptor rejeita mensagens alteradas. |
| **Masquerading (identidade forjada)** | Autenticação baseada em chave secreta única por usuário. |
| **Leitura de conteúdo (confidencialidade)** | Criptografia (DES, AES) protege o payload. |
| **Replay attacks** | **engineBoots** + **engineTime** evitam reutilização de mensagens antigas. |

*Não cobre* DoS, análise de tráfego ou ataques físicos à rede – estes são tratados por outras camadas (firewalls, QoS, etc.).  

---

## 7. Modelo de Controle de Acesso baseado em Visão (VACM)

### 7.1 Conceitos básicos

| Entidade | Descrição |
|----------|-----------|
| **User** | Identificado por *securityName* (ex.: “admin”, “monitor”). |
| **Group** | Conjunto de usuários que compartilham o mesmo nível de acesso. |
| **View** | Conjunto de OIDs (ou sub‑árvores) que podem ser lidos ou escritos. |
| **Access Right** | Permissão (read, write, notify) associada a (group, view, context). |

### 7.2 Tabelas de controle (exemplo simplificado)

| Tabela | Campos principais |
|--------|-------------------|
| **usmUserTable** (USM) | userName, authProtocol, privProtocol, authKey, privKey. |
| **vacmSecurityToGroupTable** | securityModel, securityName → groupName. |
| **vacmAccessTable** | groupName, contextPrefix, securityModel, securityLevel → readView, writeView, notifyView. |
| **vacmViewTreeFamilyTable** | viewName, subtree, mask, type (included/excluded). |

> **Operação típica:** Quando o agente recebe uma PDU, ele consulta `vacmSecurityToGroupTable` para descobrir a qual **grupo** o usuário pertence, depois verifica `vacmAccessTable` para saber quais **views** (conjuntos de OIDs) o grupo pode acessar, e finalmente usa `vacmViewTreeFamilyTable` para validar o OID solicitado.  

---

## 8. Mensagens SNMPv3 – Estrutura completa

```
+--------------------------------------------------------------+
|  Header (msgVersion, msgID, msgMaxSize, msgFlags,           |
|          msgSecurityModel, msgSecurityParameters)            |
+--------------------------------------------------------------+
|  contextEngineID   (identifica a engine que contém o MIB)   |
|  contextName       (nome lógico do contexto)                |
+--------------------------------------------------------------+
|  PDU (GetRequest, GetNextRequest, GetBulkRequest, SetRequest,|
|       InformRequest, Report, SNMPv2‑Trap)                  |
+--------------------------------------------------------------+
```

* **Report PDU** – gerada pelo agente quando ocorre um erro interno (ex.: falha de descriptografia) e o flag *reportableFlag* está setado.  
* **InformRequest** – notificação confirmada (o receptor deve responder com **Response‑PDU**).  
* **SNMPv2‑Trap** – mantido para compatibilidade, ainda sem confirmação.  

---

## 9. Fluxo típico de uma operação **Set** segura (authPriv)

1. **Gerente** cria a **SetRequest** contendo OIDs e novos valores.  
2. **Message Processing Subsystem** codifica a PDU.  
3. **Security Subsystem**:  
   - Calcula HMAC (auth) sobre a mensagem inteira (exceto o campo de autenticação).  
   - Criptografa o *Scoped PDU* (payload) usando a chave de privacidade.  
   - Preenche `msgSecurityParameters` com os parâmetros gerados.  
4. **Dispatcher** envia a mensagem via UDP (porta 161).  
5. **Agente** recebe a mensagem → **Dispatcher** encaminha ao **Message Processing**.  
6. **Security Subsystem** do agente:  
   - Descriptografa o payload (privFlag = 1).  
   - Verifica HMAC (authFlag = 1) usando a chave do usuário.  
   - Se falhar → gera **Report** (authFailure).  
7. **Access Control Subsystem** (VACM) verifica se o usuário tem permissão **write** para os OIDs.  
8. **Command Responder** executa a operação:  
   - **Fase 1 – validação** de todos os valores (tipo, tamanho, range).  
   - **Fase 2 – commit**: se tudo OK, grava as alterações; caso contrário, desfaz e devolve *commitFailed* ou *undoFailed*.  
9. **Message Processing** monta **GetResponse** contendo status e, opcionalmente, valores atuais.  
10. **Security Subsystem** adiciona HMAC e (se configurado) criptografia ao retorno.  
11. **Gerente** recebe a resposta, verifica autenticidade e, se tudo OK, confirma a mudança.  

---

## 10. RFCs principais do SNMPv3

| RFC | Tema |
|-----|------|
| **2571** | SNMP Architecture |
| **2572** | Message Processing Subsystem |
| **2573** | SNMP Engine (Dispatcher, etc.) |
| **2574** | User‑Based Security Model (USM) |
| **2575** | View‑Based Access Control Model (VACM) |
| **3410‑3418** | Atualizações e refinamentos (incluindo SNMPv3‑v2c coexistência). |

---

## 11. Principais diferenças entre **SNMPv2c** e **SNMPv3**

| Aspecto | SNMPv2c | SNMPv3 |
|---------|----------|--------|
| **Segurança** | *Community string* (texto‑claro) – apenas “read‑only”/“read‑write”. | USM (auth/priv) – HMAC + criptografia. |
| **Controle de acesso** | Nenhum (apenas comunidade). | VACM – controle granular por usuário, grupo e vista. |
| **Formato da mensagem** | Header simples (versão, comunidade, PDU). | Header complexo (msgVersion, msgID, msgFlags, …). |
| **Report PDU** | Não existe. | Existe – permite notificar erros de segurança. |
| **Compatibilidade** | Não suporta autenticação avançada. | Compatível com v1/v2c via *Security Model 1/2* (para dispositivos legados). |
| **Escalabilidade** | Limitada ao modelo “community”. | Modular – pode ser estendido (ex.: novos modelos de segurança). |

---

## 12. Pontos de atenção ao implementar SNMPv3

1. **Gerenciamento de chaves** – As chaves de autenticação e privacidade são armazenadas como *hashes* (ex.: SHA‑1). Troque-as periodicamente.  
2. **Sincronização de `engineBoots`/`engineTime`** – Se o agente reiniciar, o contador de *engineBoots* deve ser incrementado; caso contrário, o gerente rejeitará mensagens por *replay attack*.  
3. **Tamanho máximo da mensagem (`msgMaxSize`)** – Deve ser configurado para acomodar PDUs grandes (ex.: GetBulk de tabelas).  
4. **Configuração de VACM** – Defina vistas restritas (ex.: *readView* = `1.3.6.1.2.1.1` para informações de sistema, *writeView* = vazio para usuários de monitoramento).  
5. **Uso de `authPriv` sempre que possível** – Evita que informações sensíveis (ex.: contadores de tráfego) sejam interceptadas.  
6. **Teste de mensagens *Report*** – Simule falhas de autenticação para garantir que o agente gere *Report* corretamente.  

---

## 13. Conclusão

SNMPv3 representa a evolução natural do protocolo de gerenciamento de redes, mantendo a **simplicidade de operação** (PDUs semelhantes ao v2) enquanto introduz **segurança robusta** (USM) e **controle de acesso granular** (VACM).  

* A arquitetura modular permite que fabricantes e administradores escolham apenas os componentes necessários, facilitando a adoção em dispositivos de recursos limitados.  
* O modelo de segurança oferece três níveis (noAuthNoPriv, authNoPriv, authPriv) que podem ser combinados com políticas de acesso detalhadas, atendendo desde ambientes de laboratório até infraestruturas críticas.  
* A coexistência com versões anteriores (v1/v2c) garante migração suave, enquanto as extensões (Report PDU, InformRequest) aumentam a confiabilidade das notificações.  

Em resumo, **SNMPv3** fornece a base segura e flexível que as redes modernas exigem para monitoramento, configuração e diagnóstico em escala global.

---
