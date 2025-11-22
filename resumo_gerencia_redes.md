# Resumo Detalhado: Gerência de Redes de Computadores

## 1. Introdução e Conceitos Fundamentais

### 1.1 Importância da Gerência de Redes

As redes de computadores tornaram-se um **recurso estratégico crítico** para as organizações modernas. A dependência das redes é total: se a rede parar, todas as operações param. Este cenário é agravado por:

- **Escala crescente**: Data centers e infraestruturas de telecomunicações cada vez maiores
- **Complexidade**: Redes heterogêneas com múltiplas tecnologias
- **Tecnologias avançadas**: Equipamentos e protocolos cada vez mais sofisticados
- **Escassez de recursos humanos**: Falta de pessoal qualificado para gerenciar esses ambientes

### 1.2 Definição de Gerenciamento de Rede

Segundo Kurose e Ross, o gerenciamento de rede é definido como:

> "A implantação, integração e coordenação do hardware, software e elementos humanos para **monitorar, testar, contar, configurar, analisar, avaliar e controlar** a rede e os recursos para atender os requisitos de tempo real, desempenho operacional e Qualidade de Serviço a um custo razoável."

### 1.3 Conhecimento da Rede

Para gerenciar efetivamente uma rede, é fundamental **conhecê-la profundamente**:

- **Inventário completo**: Quais equipamentos compõem a rede
- **Documentação**: Diagramas e documentos atualizados da rede
- **Configurações**: Backup de todas as configurações dos equipamentos
- **Topologia**: Como os equipamentos estão interconectados
- **Registros**: Histórico de eventos e ocorrências
- **Métricas de desempenho**: 
  - Velocidade dos links
  - Throughput (taxa de transferência real)
  - Disponibilidade
  - **Baseline**: Estabelecer métricas de referência para comparação futura

---

## 2. Tarefas e Abordagens de Gerenciamento

### 2.1 Principais Tarefas de Gerenciamento

As atividades típicas incluem:

- ✅ Detecção de falhas em hardware
- ✅ Identificação de problemas de configuração
- ✅ Monitoração de tráfego para planejamento de capacidade
- ✅ Monitoração de SLAs (Service Level Agreements - Acordos de Nível de Serviço)
- ✅ Segurança e detecção de intrusos

### 2.2 Gerência Reativa vs Pró-ativa

#### **Gerência Reativa**
- O processo é acionado **após a ocorrência da falha**
- Há perda de conectividade ou queda de desempenho antes da ação
- Passos: **Detectar → Isolar → Corrigir → Documentar**
- **Limitação**: Tempo de inatividade e impacto nos usuários

#### **Gerência Pró-ativa**
- O administrador busca **continuamente** informações para antecipar problemas
- Utiliza recursos estatísticos e monitoramento diário
- Acompanha mudanças de comportamento para prever falhas
- **Vantagem**: Previne problemas antes que afetem os usuários

---

## 3. Ferramentas de Gerência

### 3.1 Ferramentas Básicas de Diagnóstico

**Características:**
- Detectam problemas simples de conectividade, disponibilidade e desempenho
- **Exemplos**: `ping`, `traceroute`, `route`, `netstat`, `ifconfig`
- **Limitação**: Baixa escalabilidade - não suportam grandes conjuntos de elementos

### 3.2 Monitores de Rede

- Conectam-se às redes e monitoram o tráfego em tempo real
- Geram estatísticas sobre:
  - Utilização da rede
  - Tipos de pacotes
  - Número de pacotes enviados/recebidos por nó
  - Pacotes com erros
- **Exemplo**: `ntop`

### 3.3 Analisadores de Rede

- Auxiliam no **rastreamento e correção** de problemas
- Permitem análise profunda de pacotes e protocolos
- **Exemplo**: `Wireshark`

### 3.4 Sistemas de Gerência de Redes (SGR)

**Características principais:**
- Monitoramento e controle de toda a rede a partir de um **ponto central** (estação de gerência)
- Interface única com informações sobre toda a rede
- Apresentação visual através de mapas da rede
- Geração automática de alarmes quando limiares são ultrapassados

**Componentes:**
- Plataforma de gerência de redes
- Aplicações de gerência de redes

**Exemplos de SGR:**

**Específicos de fornecedor:**
- DmView (Datacom)
- Cisco Prime (Cisco)

**Independentes de fornecedor:**
- *Proprietários*: Tivoli NetView (IBM), ANM (HP - antigo OpenView)
- *Software Livre*: OpenNMS, Zenoss

---

## 4. Arquitetura de Sistemas de Gerência de Redes

### 4.1 Modelo Gerente-Agente

Este é o modelo fundamental que define a arquitetura de gerência de redes.

#### **Componentes Básicos:**

1. **Elementos Gerenciados** (Objetos Gerenciados)
   - Componentes da rede que precisam operar adequadamente
   - Possuem software especial (**Agente**) para gerenciamento remoto
   - Exemplos:
     - *Hardware*: roteadores, switches, servidores, nobreaks, modems, impressoras
     - *Software*: sistemas operacionais, servidores de banco de dados, servidores web

2. **Estação de Gerência** (Gerente)
   - Contém o software que conversa com os agentes
   - Monitora e controla os componentes gerenciados
   - Interface com o usuário para facilitar a gerência
   - Funções automáticas de gerência (polling regular)

3. **Protocolo de Gerência**
   - Define as mensagens entre gerente e agentes
   - Tipos de mensagens:
     - Operações de **leitura (READ)** - monitoramento
     - Operações de **escrita (WRITE)** - controle
     - **Respostas**
     - **Notificações (traps)**
   - Exemplos de protocolos:
     - **SNMP** (Simple Network Management Protocol) - usado em redes TCP/IP
     - **SNMPv2** e **SNMPv3** - versões aprimoradas
     - **CMIP** (Common Management Information Protocol) - modelo OSI
     - **Netconf**

4. **Informações de Gerência (MIB - Management Information Base)**
   - Define os dados que podem ser referenciados nas operações
   - Conjunto das informações disponíveis em um agente
   - Exemplos de informações:
     - Erros de transmissão/recepção em enlaces
     - Status de um enlace
     - Temperatura de um roteador
     - Tensão de entrada de um nobreak

#### **Comunicação Gerente-Agente:**

**Polling (Varredura):**
- O **gerente inicia** a comunicação
- Envia periodicamente solicitações ao agente
- Agente responde com os dados solicitados
- Permite controle preciso do tráfego de gerência

**Trapping (Notificações):**
- O **agente inicia** a comunicação
- Envia notificações ao gerente quando eventos anormais ocorrem
- Eventos devem ser previamente configurados
- Reduz o tráfego de gerência, mas pode perder notificações

**Escolha entre Polling e Trapping depende de:**
- Tráfego gerado
- Robustez necessária
- Retardo aceitável
- Volume de processamento no agente/gerente
- Tipo de aplicação de monitoramento
- Consequência de uma falha no dispositivo

### 4.2 Uso de Proxies

**Função:**
- Intermediam a comunicação quando gerente e agente não falam os mesmos protocolos
- O **proxy (agente procurador)** executa em um elemento de mediação
- Traduz entre diferentes protocolos de gerência

---

## 5. Classificação das Informações de Gerência

### 5.1 Informações Estáticas
- Informações de **configuração**
- Sofrem pouca ou nenhuma alteração
- **Exemplos**: 
  - Nome dos elementos
  - Localização física
  - Endereçamento IP
  - Rotas estáticas

### 5.2 Informações Dinâmicas
- Relacionadas a **eventos na rede**
- Sofrem alterações constantes
- **Exemplos**:
  - Total de bytes enviados/recebidos
  - Total de erros
  - Tabelas de rotas dinâmicas

### 5.3 Informações Estatísticas
- **Derivadas** das informações dinâmicas
- Envolvem conceitos estatísticos (média, variância, desvio)
- **Exemplos**:
  - Taxa de utilização de largura de banda
  - Taxa de utilização de recursos (CPU, disco, memória)
  - Utilização média da rede
  - Vazão (bps)

---

## 6. Arquiteturas de Gerência de Redes

### 6.1 Arquitetura Centralizada

**Características:**
- Um **único gerente** gerencia todos os elementos
- Banco de dados único e centralizado
- Responsável por toda geração de alertas e coleta de informações

**✅ Vantagens:**
- Simplificação do processo de gerência
- Informação concentrada facilita localização e correlação de erros
- Maior segurança no acesso às informações (único ponto de controle)
- Facilita identificação de problemas correlacionados

**❌ Desvantagens:**
- Ponto único de falha (SPOF - Single Point of Failure)
- Necessidade de duplicação total da base para redundância
- Difícil expansão (baixa escalabilidade)
- Tráfego intenso concentrado no gerente

### 6.2 Arquitetura Hierárquica

**Características:**
- **SGR Servidor** centraliza informações
- Conjunto de **SGR Clientes** atuam como clientes do servidor central
- Divisão das tarefas de gerência entre servidores
- Dados ainda armazenados de forma centralizada

**✅ Vantagens:**
- Gerência não depende exclusivamente de um único sistema
- Distribuição das tarefas de gerência
- Balanceamento de tráfego entre os gerentes
- Permite gerenciar ambientes grandes com servidores de menor capacidade

**❌ Desvantagens:**
- Base de dados ainda centralizada (concentração de falhas)
- Definição da hierarquia requer planejamento cuidadoso
- Recuperação de informações mais lenta
- Possibilidade de duplicação de esforços

### 6.3 Arquitetura Distribuída

**Características:**
- Vários servidores em modelo **ponto-a-ponto**
- **Sem hierarquia** entre servidores
- **Sem centralização** da base de dados
- Cada servidor responsável por um segmento da rede
- Cada servidor possui informações de **todo o ambiente**
- Esquema de **replicação** das bases de dados

**✅ Vantagens:**
- Combina vantagens das arquiteturas centralizada e hierárquica
- Distribuição das tarefas de gerência
- Distribuição da base de dados
- Distribuição da probabilidade de falhas
- Evita dependência de um único sistema
- Análise completa do ambiente por qualquer servidor

**❌ Desvantagens:**
- Complexidade no esquema de replicação
- Necessidade de manter coerência entre bases de dados
- Maior complexidade de implementação

---

## 7. Modelo OSI de Gerência de Redes

### 7.1 Contexto e Padronização

Desenvolvido pela **ISO** (International Organization for Standardization) através do projeto OSI (Open Systems Interconnection):
- Documento: ISO 7498-4
- Reconhecido pelo **ITU-T** (recomendações série X-700)

Define **três modelos** fundamentais:
1. Modelo Organizacional
2. Modelo Informacional
3. Modelo Funcional

### 7.2 Modelo Organizacional

**Objetivo:** Estabelecer a hierarquia entre sistemas de gerência

**Conceitos principais:**
- Divide o ambiente em **domínios de gerência**
- Distribui as responsabilidades de gerência
- **NOC (Network Operation Center)**: gerencia aspectos interdomínios e enlaces que envolvem múltiplos domínios

**Justificativa:**
- Sistemas com único gerente são inapropriados para:
  - Alto volume de informações
  - Localizações geograficamente distantes
  - Necessidade de distribuição de responsabilidades

### 7.3 Modelo Informacional

**Objetivo:** Definir a estrutura dos dados de gerência

**Define:**
- **Objetos de gerência**: classes, atributos e nomes
- **Relações** entre objetos
- **Operações** sobre os objetos
- Cada objeto identificado por sequência de números (caminho desde a raiz)

**MIB (Management Information Base):**
- Armazena os objetos gerenciados
- Necessária para consulta e manipulação das informações

### 7.4 Modelo Funcional - FCAPS

Divide a gerência em **cinco áreas funcionais** fundamentais:

#### **F - Fault Management (Gerência de Falhas)**

**Objetivo:** Localizar problemas e corrigi-los

**Definição:**
- **Falha**: condição anormal que requer atenção gerencial
- Indicada por imperfeições ou erros excessivos

**Processo de Identificação:**
1. **Detecção** da falha
2. **Análise e diagnóstico**
3. **Resolução** do problema
4. **Notificação** aos interessados

**Capacidades necessárias:**
- Determinar com precisão a localização da falha
- **Isolar** o resto da rede da falha
- **Reconfigurar** a rede para minimizar impacto
- **Reparar ou substituir** o componente com problemas
- Restaurar a rede ao estado anterior

#### **C - Configuration Management (Gerência de Configuração)**

**Objetivo:** Gerenciar parâmetros de configuração dos elementos

**Atividades:**
- **Instalação** de componentes
- **Inicialização** de equipamentos
- **Modificação** de parâmetros
- **Registro** de configurações

**Exemplos práticos:**
- Configuração de componentes
- Inventário de hardware e software
- Mapeamento da topologia
- Ativação/desativação de componentes
- Controle de versões de software

#### **A - Accounting Management (Gerência de Contabilização)**

**Objetivo:** Medir utilização de recursos para contabilização

**Funcionalidades:**
- Estabelecer **métricas** de uso
- Verificar **quotas** de utilização
- Determinar **custos** de operação
- **Taxar** usuários conforme uso

**Benefícios:**
- Revelar possíveis abusos de privilégio
- Auxiliar no planejamento de capacidade
- Melhorar o desempenho através de análise de uso
- Atribuir custos e tarifas
- Emitir relatórios de utilização

#### **P - Performance Management (Gerência de Desempenho)**

**Objetivo:** Monitorar o comportamento e desempenho dos componentes

**Características:**
- Uso de **meios estatísticos** para análise
- Ações **pró-ativas** para antecipar problemas
- Estabelecimento de **limiares** (thresholds)
- Emissão de notificações quando limiares são atingidos
- Planejamento e controle da **Qualidade de Serviço (QoS)**

**Atividades:**
- Coleta de informações estatísticas:
  - Tráfego de mensagens
  - Tipo e tamanho das mensagens
  - Atraso de trânsito
- Avaliação do comportamento dos recursos
- Eficiência de utilização
- Determinação do desempenho em condições normais e de teste

**Principais Parâmetros de Desempenho:**
1. **Disponibilidade**: percentual de tempo operacional
2. **Latência**: tempo de propagação
3. **Jitter**: variação da latência
4. **Taxa de erro**: proporção de pacotes/bits com erro
5. **Vazão (Throughput)**: taxa real de transferência
6. **Utilização**: percentual de capacidade utilizada

#### **S - Security Management (Gerência de Segurança)**

**Objetivo:** Controlar acesso e garantir a política de segurança

**Funcionalidades:**
- Controlar acesso às **informações** na rede
- Controlar acesso à **rede** ou partes dela
- Garantir conformidade com a **política de segurança**
- **Coletar, armazenar e examinar**:
  - Registros de auditoria
  - Logs de segurança
- Ativar/desativar atividades de auditoria

**Importância:**
- Proteção contra acessos não autorizados
- Rastreamento de atividades suspeitas
- Conformidade regulatória
- Detecção de intrusões

---

## 8. Conclusão

A Gerência de Redes de Computadores é uma disciplina fundamental que combina aspectos técnicos, organizacionais e estratégicos. O sucesso na gerência depende de:

1. **Conhecimento profundo** da infraestrutura
2. **Ferramentas adequadas** para cada necessidade
3. **Arquitetura apropriada** ao tamanho e complexidade da rede
4. **Abordagem pró-ativa** para prevenir problemas
5. **Seguir modelos e padrões** reconhecidos (como o modelo FCAPS)
6. **Monitoramento contínuo** de métricas e desempenho
7. **Documentação rigorosa** de configurações e eventos

A evolução das redes e a crescente dependência das organizações em relação à conectividade tornam o gerenciamento de redes uma área crítica que exige profissionais qualificados e sistemas robustos de monitoramento e controle.
