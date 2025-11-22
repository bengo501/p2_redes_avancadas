# Resumo Detalhado: Introdução à Segurança da Informação e de Redes

## 1. Conceitos Fundamentais

### 1.1 Segurança Computacional
A segurança computacional é um campo abrangente que se subdivide em:
*   **Segurança da Informação**
*   **Segurança de Sistemas**
*   **Segurança de Aplicações**
*   **Segurança de Redes**

### 1.2 Segurança da Informação
A informação é um **ativo** vital para os negócios e deve ser protegida adequadamente (ABNT NBR ISO/IEC 27002:2005).

#### **Ativos**
Um ativo é qualquer coisa que tenha valor para a organização.
*   **Exemplos:** Informação eletrônica, documentos em papel, software, hardware, instalações físicas, imagem/reputação da empresa, serviços e pessoas.

### 1.3 Vulnerabilidades, Ameaças e Incidentes

| Conceito | Definição | Exemplos |
| :--- | :--- | :--- |
| **Vulnerabilidade** | Fraqueza (ponto fraco) associada a um ativo. | **Humanas:** Profissionais despreparados, usuários inexperientes.<br>**Físicas:** Falta de monitoramento, proteção inadequada, energia instável.<br>**Tecnológicas:** Software desatualizado, má configuração, falta de monitoração. |
| **Ameaça** | Possibilidade de um agente (interno ou externo) explorar uma vulnerabilidade (acidental ou propositalmente). | **Humanas:** Sabotagem, fraude, erro, descuido.<br>**Físicas:** Incêndio, inundação, apagão.<br>**Tecnológicas:** Vírus, bugs, invasão. |
| **Incidente** | Evento indesejável que causou ou pode causar dano a um ativo (consequência da exploração de uma vulnerabilidade). | Acesso não autorizado, vazamento de dados, indisponibilidade de serviço. |

**Resposta a Incidentes:** Ações tomadas após a detecção de um incidente, incluindo registro, análise forense e aplicação de medidas preventivas.

---

## 2. Organizações e Entidades de Segurança

Antigamente, apenas fabricantes rastreavam vulnerabilidades, o que gerava desorganização. Hoje, existem entidades específicas para padronizar e coordenar a segurança globalmente.

*   **CAIS (Centro de Atendimento a Incidentes de Segurança):** Responsável por incidentes na RNP (Rede Nacional de Ensino e Pesquisa), com foco no meio acadêmico brasileiro.
*   **CERT (Computer Emergency Response Team):** Centro de excelência em segurança na internet (EUA), lida com vulnerabilidades e incidentes.
*   **CERT.br:** Coordena a resposta a incidentes no Brasil, focando em prevenção e orientação para provedores e usuários.
*   **CVE (Common Vulnerabilities and Exposures):** Lista padronizada de nomes para vulnerabilidades conhecidas.
*   **MITRE ATT&CK:** Base de conhecimento global sobre táticas e técnicas usadas por invasores (Threat Intelligence).
*   **NVD (National Vulnerability Database):** Base oficial do NIST (EUA) com detalhes sobre vulnerabilidades (classificação, gravidade, etc.).

---

## 3. Segurança de Redes

Segundo William Stallings, é o conjunto de provisões e políticas para prevenir e monitorar o acesso não autorizado, uso incorreto, modificação ou negação da rede e seus recursos.

### 3.1 A Tríade CIA (Propriedades Básicas)

Os três pilares fundamentais da segurança da informação são:

#### **1. Confidencialidade (Sigilo)**
*   **Objetivo:** Garantir que a informação seja acessível apenas a usuários legítimos/autorizados.
*   **Mecanismo principal:** Criptografia e controle de acesso.

#### **2. Integridade (Consistência)**
*   **Objetivo:** Garantir que a informação mantenha seu estado original e não seja alterada indevidamente (prevenção contra criação, alteração ou destruição não autorizada).
*   **Mecanismo principal:** **Hash**.
    *   **Hash:** Sequência de bits de tamanho fixo gerada a partir de dados de qualquer tamanho por um algoritmo de dispersão. Funciona como uma "impressão digital" do arquivo.
    *   **Algoritmos comuns:**
        *   **MD5:** Gera hash de 128 bits (antigo).
        *   **SHA (Secure Hash Algorithm):** Sucessor do MD5. SHA-1 (160 bits), SHA-256, SHA-512.

#### **3. Disponibilidade (Acesso)**
*   **Objetivo:** Garantir que a informação e os ativos estejam disponíveis para usuários legítimos no momento necessário.
*   **Mecanismos:** Manutenção de hardware, backups, redundância, proteção contra ataques de negação de serviço (DoS).

---

## 4. Tipos de Ataques

Os ataques podem ser classificados de acordo com o impacto nas propriedades da segurança:

| Tipo de Ataque | Impacto Principal | Descrição |
| :--- | :--- | :--- |
| **Interrupção** | **Disponibilidade** | Um recurso é destruído ou torna-se indisponível. |
| **Intercepção** | **Confidencialidade** | Pessoa não autorizada ganha acesso a um recurso. |
| **Modificação** | **Integridade** | Pessoa não autorizada acessa e altera um recurso. |
| **Fabricação** | **Autenticidade** | Pessoa não autorizada insere objetos falsos no sistema. |

### 4.1 Classificação por Comportamento

*   **Ataques Passivos:**
    *   **Foco:** Monitoração e escuta da transmissão (obter informação).
    *   **Característica:** Não altera os dados.
    *   **Detecção/Prevenção:** Difícil de detectar, mas "fácil" de prevenir (ex: criptografia).

*   **Ataques Ativos:**
    *   **Foco:** Modificação de dados ou criação de dados falsos.
    *   **Característica:** Altera o estado do sistema ou dos dados.
    *   **Detecção/Prevenção:** Mais fácil de detectar, muito difícil de prevenir completamente.
    *   **Categorias:**
        1.  **Mascaramento:** Fingir ser outra entidade.
        2.  **Respostas forjadas (Replay):** Captura e retransmissão de mensagens válidas.
        3.  **Modificação de mensagens:** Alteração do conteúdo legítimo.
        4.  **Negação de Serviço (DoS):** Impedir o uso normal dos recursos de gestão ou rede.
