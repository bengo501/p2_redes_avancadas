# Resumo Detalhado – SNMPv2

> **Objetivo:** Apresentar, de forma estruturada, a evolução, características, novas operações e detalhes de implementação do protocolo **SNMPv2** (incluindo a variante **SNMPv2c** baseada em *community string*).

---

## 1. Histórico do SNMPv2

| Ano | Evento | Comentário |
|-----|--------|------------|
| **1993** | Definição inicial do SNMPv2 | Combinação de duas vertentes: **Secure SNMP** (propostas de segurança) e **SMP – Simple Management Protocol** (flexibilidade, eficiência e compatibilidade). |
| **1996** | Revisão do SNMPv2 | A proposta de segurança foi abandonada por falta de consenso e baixa adoção. O protocolo passou a usar apenas a *community string*, dando origem ao **SNMPv2c** ("community‑based SNMPv2"). |

> **Resultado:** SNMPv2 manteve a compatibilidade com SNMPv1, mas introduziu melhorias de desempenho e novas funcionalidades, ainda que a segurança permaneça fraca (baseada em texto‑claro). 

---

## 2. Por que o SNMPv1 precisava de evolução?

| Problema | Descrição |
|----------|-----------|
| **Ineficiência na recuperação de tabelas** | Em SNMPv1, para ler uma tabela grande (ex.: 4 colunas × 2000 linhas) era necessário fazer milhares de chamadas **GetNextRequest**, gerando grande overhead de rede e processamento. |
| **Segurança limitada** | O uso da *community string* (texto‑claro) permite que qualquer pessoa que a conheça tenha acesso total (read‑only ou read‑write) ao dispositivo. |

---

## 3. Principais características do SNMPv2

| Característica | Detalhes |
|----------------|----------|
| **Compatibilidade** | Coexiste com SNMPv1 – dispositivos podem operar simultaneamente nas duas versões. |
| **Novos tipos de dados** | Introdução de **Counter64** (64‑bit) para contadores que ultrapassam 2³²‑1. |
| **Novas macros e convenções textuais** | Facilita a definição de objetos nas MIBs (ex.: `OBJECT-TYPE`, `MODULE-IDENTITY`). |
| **Melhorias na recuperação de informações** | Operações **GetBulkRequest** e **InformRequest** reduzem o número de mensagens necessárias. |
| **Códigos de erro mais precisos** | Expansão da enumeração de erros (ex.: `noAccess`, `wrongType`, `commitFailed`, etc.). |

---

## 4. Novas Operações (PDUs) introduzidas no SNMPv2

| PDU | Número | Função | Comentário |
|-----|--------|--------|------------|
| **InformRequest** | 6 | Comunicação **gerente‑gerente** (gerente envia informação a outro gerente). | Útil em arquiteturas hierárquicas ou distribuídas; requer resposta (ack). |
| **GetBulkRequest** | 5 | Recupera **N** objetos em **uma única** mensagem, otimizando a leitura de tabelas. | Substitui múltiplas chamadas de **GetNextRequest**. |
| **Report** | — (definido, mas **não implementado**) | Mensagem interna para relatar erros excepcionais durante o processamento de requisições. |

---

## 5. Tipos de PDUs suportados pelo SNMPv2

```
0 – GetRequest
1 – GetNextRequest
2 – GetResponse
3 – SetRequest
5 – GetBulkRequest
6 – InformRequest
7 – SNMPv2‑Trap
```

*Obs.:* O **Trap** da versão 1 foi mantido, porém com o mesmo formato das demais PDUs (sem confirmação). 

---

## 6. Entidades SNMP e seus papéis

| Entidade | Pode agir como | Exemplos de comunicação |
|----------|----------------|------------------------|
| **Gerente** | Gerente, ou Gerente‑Agente | `Gerente → Agente` (Get/Set), `Gerente → Gerente` (Inform). |
| **Agente** | Agente, ou Agente‑Gerente | `Agente → Gerente` (Trap), `Agente → Agente` (informação de estado). |

> **Três tipos de acesso** possíveis: **gerente‑agente**, **gerente‑gerente** e **agente‑gerente**. 

---

## 7. Formato geral de uma PDU SNMPv2

```
+----------------------------------------------------------+
|  Version   |  Community   |  PDU (type, request‑ID, …) |
+----------------------------------------------------------+
|  VarBindList (lista de pares OID‑Valor)                 |
+----------------------------------------------------------+
```

*Campos comuns a todas as PDUs:* 
- **Version** – sempre `1` (representa SNMPv2c). 
- **Community** – string que define o nível de acesso (ex.: `public`, `private`). 
- **Request‑ID** – identificador único para correlacionar request/response. 
- **Error‑Status** – código de erro (0 = noError, 1 = tooBig, …). 
- **Error‑Index** – indica qual varbind causou o erro. 
- **VarBindList** – sequência de pares **OID** / **Valor** (valor pode ser `NULL` em Get/Next). 

---

## 8. Operações detalhadas

### 8.1 GetRequest / GetNextRequest
* **Formato e semântica** idênticos ao SNMPv1. 
* **Resposta não atômica** – o agente pode responder apenas alguns dos objetos solicitados, marcando os demais com `endOfMibView`. 
* **Tratamento de erros** – `tooBig` (PDU excede tamanho máximo) comporta‑se como no v1. 

### 8.2 SetRequest
* **Formato** idem ao v1, porém **atômico**: todas as variáveis são alteradas ou nenhuma. 
* **Processamento em duas fases:**
  1. **Validação** de cada varbind (tipo, tamanho, permissões). 
  2. **Commit** – se todas as validações passarem, as alterações são aplicadas. 
* **Erros específicos:**
  - `tooBig` – resposta não cabe no buffer. 
  - `commitFailed` – falha ao aplicar as alterações (error‑index aponta a varbind problemática). 
  - `undoFailed` – falha ao desfazer alterações já aplicadas (error‑index = 0). 

### 8.3 GetBulkRequest
* **Objetivo:** reduzir o número de mensagens ao ler grandes tabelas. 
* **Campos adicionais:**
  - **non‑repeaters (N):** número de objetos que devem ser tratados como **GetNext** simples. 
  - **max‑repetitions (M):** número máximo de repetições para os objetos restantes. 
* **Funcionamento:**
  1. O gerente envia uma lista de **(N+R)** OIDs. 
  2. Os **N** primeiros são atendidos como **GetNext** (uma única resposta). 
  3. Para cada um dos **R** objetos restantes, o agente executa **M** chamadas de **GetNext** consecutivas. 
  4. Total máximo de valores retornados = **N + (M × R)**. 

### 8.4 InformRequest
* **Comunicação gerente‑gerente** – um gerente pode notificar outro gerente sobre mudanças ou eventos. 
* **Requer confirmação** (o receptor devolve um **GetResponse**). 
* **Utilização típica:** propagação de alarmes em hierarquias de NOC, sincronização de bases de dados de gerenciamento. 

### 8.5 SNMPv2‑Trap
* Substitui o trap da versão 1, mas **mantém o mesmo formato de PDU** (sem confirmação). 
* Enviado pelo agente para o gerente (porta 162). 
* Tipos de trap padrão (ex.: `coldStart`, `linkDown`, `authenticationFailure`) permanecem. 

---

## 9. Códigos de erro ampliados (SNMPv2)

```
0  – noError
1  – tooBig
2  – noSuchName
3  – badValue
4  – readOnly
5  – genErr
6  – noAccess
7  – wrongType
8  – wrongLength
9  – wrongEncoding
10 – wrongValue
11 – noCreation
12 – inconsistentValue
13 – resourceUnavailable
14 – commitFailed
15 – undoFailed
16 – authorizationError
17 – notWritable
18 – inconsistentName
```

Esses códigos permitem ao agente informar de forma mais granular o motivo da falha, facilitando o diagnóstico e a automação de correções. 

---

## 10. Comparativo rápido SNMPv1 × SNMPv2c

| Aspecto | SNMPv1 | SNMPv2c |
|---------|--------|----------|
| **Segurança** | *Community string* (read‑only/read‑write). | Mesmo modelo de comunidade – **sem melhorias** de segurança. |
| **Operações** | Get, GetNext, Set, Trap. | Acrescenta **GetBulk**, **Inform**, **Report** (não implementado). |
| **Tipos de dados** | Inteiros de 32 bits. | Introduz **Counter64** e novos macros. |
| **Códigos de erro** | Conjunto limitado (0‑5). | Expansão para 0‑18, permitindo diagnóstico mais preciso. |
| **Eficiência** | Recuperação de tabelas lenta (múltiplos GetNext). | **GetBulk** reduz drasticamente o número de pacotes. |
| **Compatibilidade** | Compatível apenas com v1. | **Coexiste** com v1 – dispositivos podem operar em ambas as versões. |

---

## 11. Boas práticas ao usar SNMPv2c

1. **Utilizar GetBulk** sempre que precisar ler tabelas grandes.  
2. **Limitar o tamanho da comunidade** e mudar os nomes padrão (`public`, `private`) para evitar acesso não autorizado.  
3. **Monitorar erros** como `tooBig` e ajustar `msgMaxSize` nos dispositivos.  
4. **Empregar InformRequest** em arquiteturas hierárquicas para garantir entrega confiável de notificações.  
5. **Planejar migração** para SNMPv3 quando a segurança for requisito crítico, pois SNMPv2c ainda depende de texto‑claro. 

---

## 12. Conclusão

O **SNMPv2** (principalmente na variante **SNMPv2c**) trouxe melhorias significativas em relação ao SNMPv1, sobretudo na **eficiência de coleta de dados** (GetBulk) e na **expressividade dos códigos de erro**. Contudo, a **segurança** permaneceu vulnerável, pois continuou a usar a *community string* em texto‑claro. Para ambientes que exigem apenas monitoramento básico e alta compatibilidade, SNMPv2c ainda pode ser adequado, mas a migração para **SNMPv3** é recomendada sempre que a integridade, autenticidade ou confidencialidade dos dados de gerenciamento forem críticas.

---
