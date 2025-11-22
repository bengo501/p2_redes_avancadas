# Resumo Detalhado: MIB e SMI

## 1. Introdução à Arquitetura de Gerenciamento Internet

### 1.1 Visão Geral do Modelo

A arquitetura de gerenciamento de redes na Internet baseia-se em três componentes principais que trabalham em conjunto:

```
┌─────────────────┐
│     Gerente     │ ←─── Managing Server/Controller
│  (Controller)   │
└────────┬────────┘
         │
    Protocolo SNMP
         │
    ┌────┴─────────────────────────────────┐
    │                                      │
┌───▼──────┐  ┌──────────┐  ┌──────────┐
│  Agente  │  │  Agente  │  │  Agente  │
│   MIB    │  │   MIB    │  │   MIB    │
└──────────┘  └──────────┘  └──────────┘
Managed       Managed       Managed
Device        Device        Device
```

**Componentes:**
1. **Gerente (Manager)**: Servidor/controlador de gerenciamento
2. **Agente (Agent)**: Software nos dispositivos gerenciados
3. **Protocolo**: SNMP para comunicação
4. **MIB**: Base de dados com objetos gerenciados

---

## 2. MIB - Management Information Base

### 2.1 Conceito e Definição

A **MIB (Management Information Base)** é uma **base de dados conceitual** que define os objetos (variáveis) que podem ser monitorados e gerenciados em um dispositivo de rede.

**Características principais:**
- É uma estrutura **conceitual**, não física
- Os dados reais podem estar nos próprios recursos do dispositivo
- Exemplo: o estado atual de uma interface de rede
- Organizada em **estrutura hierárquica de árvore**

### 2.2 Evolução Histórica

**MIB I (RFC 1158):**
- Primeira versão padronizada
- Posteriormente substituída

**MIB II (RFC 1213):**
- Versão atual e mais utilizada
- Expandiu e melhorou a MIB I
- Define objetos agrupados em categorias lógicas

### 2.3 Informações Disponíveis na MIB

Através dos objetos disponíveis em uma MIB, é possível acessar diversas informações sobre o dispositivo:

- ✅ **Nome do dispositivo**
- ✅ **Versão de software** utilizado
- ✅ **Número de interfaces** presentes no equipamento
- ✅ **Número de pacotes por segundo** que passam por uma interface
- ✅ **Status operacional** de componentes
- ✅ **Estatísticas de tráfego** e erros
- ✅ **Configurações** diversas

### 2.4 Estrutura em Árvore da MIB

A MIB é apresentada como uma **árvore de dados estruturada** onde:

**Nodos Intermediários:**
- Contêm **sub-nodos**
- **Não possuem valores** associados
- Servem apenas para organização hierárquica

**Objetos (Nodos Folha):**
- **Não possuem sub-nodos**
- Possuem um **valor associado**
- São os dados que podem ser consultados/modificados

**Exemplo visual da estrutura:**

```
        Raiz
         │
    ┌────┴────┐
Nodo(1)    Nodo(2)
    │          │
Nodo(1)    Nodo(1)──┬──Nodo(2)
    │              │        │
Objeto(1)      Objeto(2) Objeto(1)
```

### 2.5 OID - Object Identifier

#### 2.5.1 O que é um OID?

Cada nodo na árvore MIB possui um **identificador único** chamado **OID (Object Identifier)**.

**Composição do OID:**
- O OID de um nodo é formado pelo **OID do nodo pai** + **identificador relativo próprio**
- O nodo raiz **não possui OID**
- A árvore é percorrida em **profundidade**, começando pelos ramos da esquerda seguindo para a direita

#### 2.5.2 Formato Numérico dos OIDs

Os OIDs são representados como sequências de números separados por pontos:

**Exemplo:**
```
1.3.6.1.2.1.1
```

**Problema:** O uso de números dificulta a compreensão do significado de cada nodo.

#### 2.5.3 OID Name - Nomes Descritivos

Para melhorar a legibilidade, os OIDs podem ser substituídos por **nomes descritivos**:

**Exemplos:**
- `system = 1.3.6.1.2.1.1`
- `sysUpTime = 1.3.6.1.2.1.1.3`

#### 2.5.4 Notação Mista

OID numérico e nome descritivo podem ser **combinados** para facilitar o entendimento:

**Exemplo:**
```
sysUpTime = system.3
```
Onde:
- `system` corresponde a `1.3.6.1.2.1.1`
- `.3` é o identificador relativo
- Resultado completo: `1.3.6.1.2.1.1.3`

### 2.6 Arquivo de MIB

#### 2.6.1 O que é um Arquivo de MIB?

Um arquivo de MIB é um **documento que descreve** a base de dados conceitual:

**Conteúdo do arquivo:**
- ✅ Descrição de cada dado (objeto)
- ✅ Tipo de cada objeto
- ✅ Estruturação dentro da árvore hierárquica
- ✅ Relações entre objetos

**Importante:** 
- O arquivo MIB contém apenas a **definição** dos objetos
- Os **valores reais** são recuperados através do acesso aos agentes nos dispositivos

### 2.7 Estrutura Hierárquica da MIB - Árvore Completa

#### 2.7.1 Raiz da Árvore MIB

A MIB é dividida em **três sub-árvores principais** na raiz:

```
         Raiz
          │
    ┌─────┼─────┐
    │     │     │
ccitt   iso   joint-iso-ccitt
 (0)    (1)       (2)
```

**Administração:**
- **ccitt (0)**: Administrada pelo CCITT
- **iso (1)**: Administrada pela ISO
- **joint-iso-ccitt (2)**: Administrada conjuntamente por ISO e CCITT

#### 2.7.2 Sub-árvore Internet

A gerência de redes Internet utiliza o ramo:

```
iso (1) → org (3) → dod (6) → internet (1)
```

**Caminho completo:** `1.3.6.1`

Onde:
- **iso (1)**: International Standards Organization
- **org (3)**: Organizações
- **dod (6)**: U.S. Department of Defense
- **internet (1)**: Internet

#### 2.7.3 Sub-árvores sob Internet

Sob o nodo `internet (1)`, temos **quatro ramos principais**:

```
         internet (1)
              │
    ┌─────┬───┴───┬─────┐
    │     │       │     │
directory mgmt experimental private
   (1)    (2)      (3)     (4)
```

**Funcionalidades:**

1. **directory (1)**: 
   - Reservado para uso futuro da ISO
   - Relacionado a serviços de diretório

2. **mgmt (2)**: 
   - Para **gerenciamento genérico**
   - Contém a MIB II
   - Objetos padronizados para todos os dispositivos

3. **experimental (3)**: 
   - Para **experimentações**
   - Novos objetos sendo testados

4. **private (4)**: 
   - Para **gerenciamento específico**
   - Contém **enterprises (1)**
   - MIBs proprietárias de fabricantes

#### 2.7.4 Estrutura da MIB II

Sob `mgmt (2)` temos `mib2 (1)`, que contém os **grupos principais** de objetos:

```
                    mib2 (1)
                 1.3.6.1.2.1
                      │
    ┌────┬────┬────┬──┴──┬────┬────┬────┬────┬────┐
    │    │    │    │     │    │    │    │    │    │
 system interfaces at  ip  icmp tcp udp egp transmission snmp
  (1)     (2)    (3) (4)  (5)  (6) (7) (8)    (9)      (10)
```

### 2.8 Grupos da MIB II - Detalhamento

#### **1. system (1)** - Informações Gerais do Sistema
OID Base: `1.3.6.1.2.1.1`

Objetos principais:
- **sysDescr**: Descrição textual do dispositivo
- **sysContact**: Informações de contato do responsável
- **sysLocation**: Localização física do equipamento
- **sysName**: Nome atribuído ao sistema

#### **2. interfaces (2)** - Interfaces de Rede
OID Base: `1.3.6.1.2.1.2`

Objetos principais:
- **ifDescr**: Descrição da interface
- **ifType**: Tipo da interface (Ethernet, Serial, etc.)
- **ifSpeed**: Velocidade da interface
- **ifPhysAddress**: Endereço físico (MAC)

#### **3. at (3)** - Address Translation (Deprecated)
OID Base: `1.3.6.1.2.1.3`

Objetos:
- **atPhysAddress**: Endereço físico
- **atNetAddress**: Endereço de rede

#### **4. ip (4)** - Protocolo IP
OID Base: `1.3.6.1.2.1.4`

Objetos principais:
- **ipForwarding**: Indica se o IP forwarding está ativo
- **ipInReceives**: Pacotes IP recebidos
- **ipInDiscards**: Pacotes descartados
- **ipOutRequests**: Pacotes enviados

#### **5. icmp (5)** - Protocolo ICMP
OID Base: `1.3.6.1.2.1.5`

Objetos principais:
- **icmpInMsgs**: Mensagens ICMP recebidas
- **icmpInErrors**: Erros ICMP recebidos
- **icmpInEchos**: Echo requests recebidos

#### **6. tcp (6)** - Protocolo TCP
OID Base: `1.3.6.1.2.1.6`

Objetos principais:
- **tcpMaxConn**: Número máximo de conexões
- **tcpInErrs**: Erros TCP

#### **7. udp (7)** - Protocolo UDP
OID Base: `1.3.6.1.2.1.7`

Objetos principais:
- **udpInDatagrams**: Datagramas UDP recebidos
- **udpNoPorts**: Datagramas sem porta de destino

#### **8. egp (8)** - Protocolo EGP
OID Base: `1.3.6.1.2.1.8`

Objetos principais:
- **egpNeighAS**: AS do vizinho EGP
- **egpNeighInMsgs**: Mensagens recebidas do vizinho

#### **9. transmission (9)** - Tecnologias de Transmissão
OID Base: `1.3.6.1.2.1.9`

Informações específicas sobre meios de transmissão.

#### **10. snmp (10)** - Protocolo SNMP
OID Base: `1.3.6.1.2.1.10`

Objetos principais:
- **snmpInPkts**: Pacotes SNMP recebidos
- **snmpOutPkts**: Pacotes SNMP enviados

### 2.9 Exemplo de OID Completo

**Objeto:** `sysDescr`
**OID Completo:** `1.3.6.1.2.1.1.1`

**Decomposição:**
```
1       - iso
  3     - org
    6   - dod
      1 - internet
        2   - mgmt
          1 - mib2
            1   - system
              1 - sysDescr
```

---

## 3. SMI - Structure of Management Information

### 3.1 Definição e Propósito

**SMI (Structure of Management Information)** é um **conjunto de regras** que define como uma MIB é especificada.

**Função principal:**
- Define a **sintaxe** e **semântica** para descrição de objetos MIB
- Estabelece **regras de estruturação** dos dados
- Garante **consistência** entre diferentes MIBs

### 3.2 Relação entre SMI, ASN.1 e MIB

```
┌─────────────────────────────────────┐
│   Arquivo de MIB                    │
│                                     │
│   Usa:                              │
│   • Notação ASN.1                   │
│   • Regras SMI                      │
│                                     │
│   Para definir:                     │
│   • Objetos da MIB                  │
└─────────────────────────────────────┘
```

### 3.3 Três Componentes Essenciais do SMI

Todo objeto da MIB **deve possuir** três elementos obrigatórios:

#### 3.3.1 Nome (OID)
- **Identificador único** do objeto
- Formato numérico hierárquico
- Exemplo: `1.3.6.1.2.1.1.1`

#### 3.3.2 Sintaxe
- Define o **tipo do objeto**
- Tipos básicos:
  - **INTEGER**: Número inteiro
  - **OCTET STRING**: Sequência de bytes
  - **OBJECT IDENTIFIER**: Referência a outro objeto
  - **NULL**: Valor nulo
  - **IpAddress**: Endereço IP
  - **Counter**: Contador crescente (32 bits)
  - **Gauge**: Valor não-negativo que pode aumentar/diminuir
  - **TimeTicks**: Valor de tempo
  - **DisplayString**: Texto ASCII

#### 3.3.3 Codificação
- Descreve **como as informações serão transmitidas** pela rede
- Utiliza **BER (Basic Encoding Rules)** do ASN.1
- Define representação binária dos dados

### 3.4 ASN.1 - Abstract Syntax Notation One

**O que é ASN.1?**
- Linguagem de notação para definir estruturas de dados
- Independente de plataforma e linguagem de programação
- Utilizada para descrever objetos MIB

**SMI usa um sub-conjunto de ASN.1:**
- Não utiliza todos os recursos do ASN.1
- Restringe-se a tipos e construções específicas

### 3.5 Elementos do ASN.1 Usados em SMI

#### 3.5.1 Tipos e Valores
- **Tipo**: Define uma **classe** de dados
- **Valor**: Representa uma **instância** dessa classe

**Exemplo:**
```
Tipo: INTEGER
Valor: 42
```

#### 3.5.2 Macros
- **Mecanismos que auxiliam** na definição dos objetos MIB
- Permitem **expansão do ASN.1**
- Fornecem estrutura padronizada

**Macro mais importante:** `OBJECT-TYPE`

### 3.6 Macro OBJECT-TYPE

A macro **OBJECT-TYPE** é usada **extensivamente** na definição de MIBs.

#### 3.6.1 Estrutura da Macro OBJECT-TYPE

```asn1
<nome> OBJECT-TYPE
    SYNTAX <tipo>
    ACCESS <modo de acesso>
    STATUS <status>
    DESCRIPTION "<descrição>"
    ::= { <pai> <número> }
```

#### 3.6.2 Campos da Macro OBJECT-TYPE

**1. Nome do Objeto:**
- Identificador textual do objeto
- Exemplo: `sysDescr`, `ifSpeed`

**2. SYNTAX:**
- Tipo de dados do objeto
- Exemplos: `INTEGER`, `Counter`, `DisplayString`, `IpAddress`
- Pode incluir restrições (ex: tamanho)

**3. ACCESS:**
Define o modo de acesso ao objeto:
- **read-only**: Apenas leitura
- **read-write**: Leitura e escrita
- **write-only**: Apenas escrita (raro)
- **not-accessible**: Não acessível diretamente

**4. STATUS:**
Indica o status do objeto na especificação:
- **mandatory**: Obrigatório (deve ser implementado)
- **optional**: Opcional
- **obsolete**: Obsoleto (não deve ser implementado)
- **deprecated**: Descontinuado (pode ser removido)

**5. DESCRIPTION:**
- Descrição textual do objeto
- Explica o propósito e uso do objeto

**6. Atribuição (::=):**
- Define a posição na árvore MIB
- `{ <pai> <número> }`: Nodo pai e identificador relativo

#### 3.6.3 Exemplo Completo: sysDescr

```asn1
sysDescr OBJECT-TYPE
    SYNTAX DisplayString (SIZE(0..255))
    ACCESS read-only
    STATUS mandatory
    DESCRIPTION 
        "A textual description of the entity. This value 
         should include the full name and version 
         identification of the system's hardware type, 
         software operating-system, and networking software."
    ::= { system 1 }
```

**Interpretação:**
- **Nome**: `sysDescr`
- **Tipo**: String de exibição com 0 a 255 caracteres
- **Acesso**: Somente leitura
- **Status**: Obrigatório
- **Descrição**: Descrição textual do dispositivo
- **Posição**: Primeiro objeto do grupo `system`
- **OID**: `system.1` ou `1.3.6.1.2.1.1.1`

---

## 4. Exemplo Prático: MIB Customizada

### 4.1 Cenário

**Empresa:** XYZ Corp.
**Necessidade:** Gerenciar servidores de arquivos

**Ambiente:**
```
┌──────────────┐
│   Gerente    │
│   Estação    │
│   Windows    │
└──────┬───────┘
       │ SNMP
   ┌───┴────────────────┐
   │                    │
┌──▼──────────┐  ┌──────▼───┐
│ Servidor    │  │  File    │
│ Unix        │  │  Server  │
└─────────────┘  └──────────┘
    XYZ Corp.
```

### 4.2 Objetos a Serem Gerenciados

A empresa deseja monitorar:

1. **Arquivos enviados** (contador)
2. **Endereço do servidor remoto** (IP)
3. **Porta do servidor remoto** (número)
4. **Porta do servidor local** (número)

### 4.3 Definição do Arquivo MIB

**Nome do arquivo:** `XYZCORP-FILESERVER-MIB.my`

```asn1
XYZCorp-MIB DEFINITIONS ::= BEGIN

-- =====================================================
-- IMPORTS: Importação de tipos e definições
-- =====================================================
IMPORTS
    Counter, Gauge          FROM RFC1155-SMI
    OBJECT-TYPE            FROM RFC-1212
    experimental           FROM RFC1155-SMI;

-- =====================================================
-- DEFINIÇÃO DA RAIZ DA MIB CUSTOMIZADA
-- =====================================================
XYZCorp OBJECT IDENTIFIER ::= { experimental 57 }

-- =====================================================
-- DEFINIÇÃO DO GRUPO fileServer
-- =====================================================
fileServer OBJECT IDENTIFIER ::= { XYZCorp 1 }
-- OID completo: 1.3.6.1.3.57.1

-- =====================================================
-- OBJETO 1: Contador de Arquivos Enviados
-- =====================================================
fsFilesSent OBJECT-TYPE
    SYNTAX Counter
    ACCESS read-only
    STATUS mandatory
    DESCRIPTION 
        "Número total de arquivos enviados pelo servidor.
         Este valor é incrementado a cada arquivo 
         transferido com sucesso."
    ::= { fileServer 1 }
-- OID: 1.3.6.1.3.57.1.1

-- =====================================================
-- OBJETO 2: Endereço IP do Servidor Remoto
-- =====================================================
fsRemoteServer OBJECT-TYPE
    SYNTAX IpAddress
    ACCESS read-write
    STATUS mandatory
    DESCRIPTION 
        "Endereço IP do servidor remoto ao qual este 
         servidor de arquivos se conecta para 
         transferências."
    ::= { fileServer 2 }
-- OID: 1.3.6.1.3.57.1.2

-- =====================================================
-- OBJETO 3: Porta do Servidor Remoto
-- =====================================================
fsRemoteServerPort OBJECT-TYPE
    SYNTAX Gauge
    ACCESS read-write
    STATUS mandatory
    DESCRIPTION 
        "Número da porta TCP/UDP utilizada para conexão 
         com o servidor remoto."
    ::= { fileServer 3 }
-- OID: 1.3.6.1.3.57.1.3

-- =====================================================
-- OBJETO 4: Porta do Servidor Local
-- =====================================================
fsLocalServerPort OBJECT-TYPE
    SYNTAX Gauge
    ACCESS read-write
    STATUS mandatory
    DESCRIPTION 
        "Número da porta TCP/UDP na qual o servidor local 
         escuta conexões para transferência de arquivos."
    ::= { fileServer 4 }
-- OID: 1.3.6.1.3.57.1.4

END
```

### 4.4 Análise Detalhada do Exemplo

#### 4.4.1 Seção IMPORTS

```asn1
IMPORTS
    Counter, Gauge          FROM RFC1155-SMI
    OBJECT-TYPE            FROM RFC-1212
    experimental           FROM RFC1155-SMI;
```

**Importa definições de outras MIBs:**
- **Counter, Gauge**: Tipos de dados numéricos
- **OBJECT-TYPE**: Macro para definir objetos
- **experimental**: Ramo da árvore MIB para experimentações

#### 4.4.2 Definição da Raiz Customizada

```asn1
XYZCorp OBJECT IDENTIFIER ::= { experimental 57 }
```

- Cria um nodo **XYZCorp** sob o ramo **experimental**
- OID: `1.3.6.1.3.57`
- Número 57 escolhido arbitrariamente (em produção, seria registrado)

#### 4.4.3 Grupo fileServer

```asn1
fileServer OBJECT IDENTIFIER ::= { XYZCorp 1 }
```

- Cria um grupo para objetos relacionados a servidores de arquivos
- OID: `1.3.6.1.3.57.1`

#### 4.4.4 Tipo Counter vs Gauge

**Counter:**
- Contador que **só aumenta** (nunca diminui)
- Reseta quando atinge valor máximo (32 bits)
- Ideal para: total de arquivos enviados, pacotes transmitidos
- **Uso no exemplo**: `fsFilesSent`

**Gauge:**
- Valor que pode **aumentar ou diminuir**
- Representa um valor instantâneo
- Ideal para: números de porta, largura de banda atual
- **Uso no exemplo**: `fsRemoteServerPort`, `fsLocalServerPort`

#### 4.4.5 Tipo IpAddress

```asn1
SYNTAX IpAddress
```

- Tipo especial para endereços IP
- Representa endereço IPv4 (4 bytes)
- **Uso no exemplo**: `fsRemoteServer`

#### 4.4.6 Modos de Acesso

**read-only** (`fsFilesSent`):
- Gerente pode apenas **consultar** o valor
- Não pode modificar
- Apropriado para contadores e estatísticas

**read-write** (`fsRemoteServer`, `fsRemoteServerPort`, `fsLocalServerPort`):
- Gerente pode **consultar e modificar** o valor
- Permite configuração remota
- Apropriado para parâmetros de configuração

### 4.5 Estrutura Hierárquica do Exemplo

```
experimental (3)
    │
    └── XYZCorp (57)
            │
            └── fileServer (1)
                    │
                    ├── fsFilesSent (1)
                    ├── fsRemoteServer (2)
                    ├── fsRemoteServerPort (3)
                    └── fsLocalServerPort (4)
```

### 4.6 Casos de Uso

#### Consulta SNMP (GET)
```
Gerente → Agente: GET 1.3.6.1.3.57.1.1
Agente → Gerente: Valor = 1523 (arquivos enviados)
```

#### Configuração SNMP (SET)
```
Gerente → Agente: SET 1.3.6.1.3.57.1.2 = 192.168.1.100
Agente → Gerente: OK (endereço remoto configurado)
```

---

## 5. Resumo e Conceitos-Chave

### 5.1 Relacionamento entre Componentes

```
┌─────────────────────────────────────────────┐
│  Gerenciamento SNMP                         │
├─────────────────────────────────────────────┤
│                                             │
│  ┌──────────┐    Consulta    ┌──────────┐  │
│  │ Gerente  │ ─────────────→ │  Agente  │  │
│  │          │ ←───────────── │          │  │
│  └──────────┘    Resposta    └────┬─────┘  │
│                                    │        │
│                              ┌─────▼─────┐  │
│                              │    MIB    │  │
│                              │ (objetos) │  │
│                              └───────────┘  │
│                                             │
│  MIB definida usando:                       │
│  • SMI (regras)                             │
│  • ASN.1 (notação)                          │
│  • Macro OBJECT-TYPE                        │
└─────────────────────────────────────────────┘
```

### 5.2 Pontos Essenciais

#### **MIB:**
- ✅ Base de dados **conceitual** hierárquica
- ✅ Organizada em **árvore** de objetos
- ✅ Cada objeto tem **OID único**
- ✅ Divide-se em grupos lógicos (system, interfaces, ip, etc.)
- ✅ MIB II (RFC 1213) é o padrão atual

#### **SMI:**
- ✅ Define **regras** para especificação de MIBs
- ✅ Utiliza **sub-conjunto de ASN.1**
- ✅ Todo objeto precisa: **nome, sintaxe, codificação**
- ✅ Macro **OBJECT-TYPE** é fundamental

#### **OID:**
- ✅ Identificador **numérico hierárquico**
- ✅ Pode ter **nome descritivo**
- ✅ Formato: sequência de números separados por pontos
- ✅ Exemplo: `1.3.6.1.2.1.1.1` ou `sysDescr`

#### **Arquivo MIB:**
- ✅ Descreve a **estrutura** dos dados
- ✅ Usa notação **ASN.1** com regras **SMI**
- ✅ Define objetos com **OBJECT-TYPE**
- ✅ Valores reais obtidos via **SNMP** do agente

### 5.3 Fluxo de Trabalho

1. **Definição**: Criar arquivo MIB usando ASN.1 e SMI
2. **Implementação**: Agente implementa objetos definidos
3. **Compilação**: Gerente carrega e compila o arquivo MIB
4. **Gerenciamento**: Gerente consulta/modifica objetos via SNMP
5. **Resposta**: Agente acessa recursos e responde

### 5.4 Benefícios da Padronização MIB/SMI

- 🎯 **Interoperabilidade**: Equipamentos de diferentes fabricantes
- 🎯 **Consistência**: Estrutura uniforme de dados
- 🎯 **Extensibilidade**: Fácil adicionar novos objetos (MIBs privadas)
- 🎯 **Organização**: Estrutura hierárquica clara
- 🎯 **Manutenção**: Documentação padronizada

---

## 6. Conclusão

A **MIB** e o **SMI** formam a base da gerência de redes usando SNMP. A compreensão desses conceitos é fundamental para:

- 📊 **Monitorar** dispositivos de rede eficientemente
- ⚙️ **Configurar** equipamentos remotamente
- 🔍 **Diagnosticar** problemas na infraestrutura
- 📈 **Coletar** estatísticas para análise de desempenho
- 🛠️ **Criar** MIBs customizadas para necessidades específicas

A estrutura hierárquica, combinada com a padronização do SMI e a flexibilidade do ASN.1, permite que a gerência SNMP seja escalável, extensível e amplamente adotada em ambientes corporativos de todos os tamanhos.
