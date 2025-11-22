import json
import os

# Ler o bundle de conteúdos
with open('content_bundle.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Criar um dicionário { "nome_arquivo": "conteúdo" }
md_content_map = {item['Name']: item['Content'] for item in data}

# Converter para string JSON para injeção no JS
json_content_string = json.dumps(md_content_map, ensure_ascii=False)

# Template HTML
html_template = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <title>Redes Avançadas – Visão Geral</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 0;
            background: #f4f7fa;
            color: #333;
        }
        header {
            background: linear-gradient(135deg, #2c3e50, #4ca1af);
            color: white;
            padding: 2rem 1rem;
            text-align: center;
        }
        header h1 { margin: 0; font-size: 2.5rem; }
        header p { opacity: 0.9; font-size: 1.1rem; }
        nav {
            background: #fff;
            border-bottom: 1px solid #ddd;
            padding: 0.5rem 1rem;
            position: sticky;
            top: 0;
            z-index: 100;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            display: flex;
            justify-content: center;
            flex-wrap: wrap;
        }
        nav a {
            margin: 0.5rem 1rem;
            color: #2c3e50;
            text-decoration: none;
            font-weight: 600;
            transition: color 0.2s;
        }
        nav a:hover { color: #4ca1af; text-decoration: underline; }
        main { padding: 2rem; max-width: 1200px; margin: auto; }
        
        /* Section Styling */
        section { margin-bottom: 3rem; scroll-margin-top: 80px; }
        h2 { 
            border-left: 5px solid #4ca1af; 
            padding-left: 1rem; 
            color: #2c3e50; 
            font-size: 1.8rem;
            margin-bottom: 1.5rem;
        }
        h3 { color: #34495e; margin-top: 1.5rem; }

        /* Grid Layout for Cards */
        .grid-container {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 1.5rem;
        }

        .card {
            background: white;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
            padding: 1.5rem;
            transition: transform 0.2s, box-shadow 0.2s;
            border: 1px solid #eee;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }
        .card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 15px rgba(0,0,0,0.1);
        }
        .card h4 { margin: 0 0 0.5rem 0; color: #2c3e50; font-size: 1.2rem; }
        .card p { color: #666; font-size: 0.95rem; flex-grow: 1; margin-bottom: 1rem; }
        
        .btn-group {
            display: flex;
            gap: 10px;
            margin-top: auto;
        }
        .btn {
            flex: 1;
            padding: 0.5rem;
            text-decoration: none;
            border-radius: 5px;
            text-align: center;
            font-weight: 500;
            transition: background 0.2s;
            font-size: 0.9rem;
        }
        .btn-primary {
            background: #4ca1af;
            color: white;
        }
        .btn-primary:hover { background: #3b8d99; }
        .btn-secondary {
            background: #ecf0f1;
            color: #2c3e50;
            border: 1px solid #bdc3c7;
        }
        .btn-secondary:hover { background: #bdc3c7; }

        /* Mermaid Diagram */
        .mermaid-container {
            background: white;
            padding: 2rem;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
            text-align: center;
            overflow-x: auto;
        }

        /* Modal Styling */
        .modal {
            display: none;
            position: fixed;
            z-index: 1000;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            overflow: auto;
            background-color: rgba(0,0,0,0.5);
            backdrop-filter: blur(5px);
        }
        .modal-content {
            background-color: #fefefe;
            margin: 5% auto;
            padding: 0;
            border: 1px solid #888;
            width: 80%;
            max-width: 900px;
            border-radius: 10px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.3);
            animation: slideIn 0.3s;
        }
        @keyframes slideIn {
            from {transform: translateY(-50px); opacity: 0;}
            to {transform: translateY(0); opacity: 1;}
        }
        .modal-header {
            padding: 1rem 1.5rem;
            background: #f4f7fa;
            border-bottom: 1px solid #ddd;
            border-radius: 10px 10px 0 0;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .modal-header h2 { margin: 0; font-size: 1.5rem; border: none; padding: 0; }
        .close {
            color: #aaa;
            font-size: 28px;
            font-weight: bold;
            cursor: pointer;
        }
        .close:hover { color: black; }
        .modal-body {
            padding: 2rem;
            line-height: 1.6;
            color: #444;
            max-height: 70vh;
            overflow-y: auto;
        }
        /* Markdown Content Styling inside Modal */
        .modal-body h1, .modal-body h2, .modal-body h3 { color: #2c3e50; margin-top: 1.5rem; }
        .modal-body h1 { border-bottom: 2px solid #4ca1af; padding-bottom: 0.5rem; }
        .modal-body h2 { border-left: 4px solid #4ca1af; padding-left: 10px; }
        .modal-body code { background: #f4f4f4; padding: 2px 5px; border-radius: 3px; font-family: monospace; color: #e74c3c; }
        .modal-body pre { background: #2d3436; color: #dfe6e9; padding: 1rem; border-radius: 5px; overflow-x: auto; }
        .modal-body pre code { background: none; color: inherit; }
        .modal-body blockquote { border-left: 4px solid #bdc3c7; margin: 0; padding-left: 1rem; color: #7f8c8d; font-style: italic; }
        .modal-body table { width: 100%; border-collapse: collapse; margin: 1rem 0; }
        .modal-body th, .modal-body td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        .modal-body th { background-color: #f2f2f2; color: #2c3e50; }

        footer {
            text-align: center;
            padding: 2rem;
            background: #2c3e50;
            color: #ecf0f1;
            margin-top: 3rem;
        }
    </style>
    <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
    <script>
        mermaid.initialize({ startOnLoad:true, theme: 'neutral' });

        // INJECTED_CONTENT_HERE
        const markdownFiles = %s;

        function openModal(fileName, title) {
            const modal = document.getElementById('contentModal');
            const modalTitle = document.getElementById('modalTitle');
            const modalBody = document.getElementById('modalBody');
            
            modalTitle.innerText = title;
            modalBody.innerHTML = '<p>Carregando...</p>';
            modal.style.display = "block";

            const content = markdownFiles[fileName];
            
            if (content) {
                modalBody.innerHTML = marked.parse(content);
            } else {
                modalBody.innerHTML = '<p style="color:red">Conteúdo não encontrado.</p>';
            }
        }

        function closeModal() {
            document.getElementById('contentModal').style.display = "none";
        }

        window.onclick = function(event) {
            const modal = document.getElementById('contentModal');
            if (event.target == modal) {
                modal.style.display = "none";
            }
        }
    </script>
</head>
<body>
    <header>
        <h1>Redes Avançadas – Visão Geral</h1>
        <p>Gerência de Redes & Segurança da Informação</p>
    </header>
    <nav>
        <a href="#diagrama">Mapa Mental</a>
        <a href="#gerencia">Gerência de Redes</a>
        <a href="#seguranca">Segurança de Redes</a>
    </nav>
    <main>
        <!-- Diagrama Mermaid -->
        <section id="diagrama">
            <h2>Mapa de Conteúdos</h2>
            <div class="mermaid-container">
                <div class="mermaid">
                mindmap
                  root((Redes Avançadas))
                    Gerência de Redes
                      Resumo: Gerência
                      Resumo: MIB e SMI
                      Resumo: SNMP v1
                      Resumo: SNMPv2
                      Resumo: SNMPv3
                      Exercícios SNMP
                    Segurança de Redes
                      Introdução à Segurança
                      Segurança em Camadas
                      Vulnerabilidades e Ataques
                      Proteção e Defesa
                      Caso NotPetya
                      Exercícios CERT.br
                      Exercícios Práticos
                </div>
            </div>
        </section>
        
        <!-- Seção de Gerência -->
        <section id="gerencia">
            <h2>📡 Gerência de Redes</h2>
            <div class="grid-container">
                <!-- Card 1 -->
                <div class="card">
                    <h4>Resumo – Gerência de Redes</h4>
                    <p>Conceitos fundamentais, arquiteturas (centralizada, hierárquica, distribuída), modelo OSI e FCAPS.</p>
                    <div class="btn-group">
                        <a href="resumo_gerencia_redes.md" target="_blank" class="btn btn-secondary">Ver Arquivo Original</a>
                        <a href="#" onclick="openModal('resumo_gerencia_redes.md', 'Resumo – Gerência de Redes'); return false;" class="btn btn-primary">Ler Modo Visual</a>
                    </div>
                </div>
                <!-- Card 2 -->
                <div class="card">
                    <h4>Resumo – MIB e SMI</h4>
                    <p>Estrutura de árvores OID, definição de objetos, macros OBJECT‑TYPE e exemplo de MIB customizada.</p>
                    <div class="btn-group">
                        <a href="resumo_mib_smi.md" target="_blank" class="btn btn-secondary">Ver Arquivo Original</a>
                        <a href="#" onclick="openModal('resumo_mib_smi.md', 'Resumo – MIB e SMI'); return false;" class="btn btn-primary">Ler Modo Visual</a>
                    </div>
                </div>
                <!-- Card 3 -->
                <div class="card">
                    <h4>Resumo – SNMP (v1)</h4>
                    <p>Arquitetura gerente‑agente, PDUs básicas, segurança por community string.</p>
                    <div class="btn-group">
                        <a href="resumo_snmp.md" target="_blank" class="btn btn-secondary">Ver Arquivo Original</a>
                        <a href="#" onclick="openModal('resumo_snmp.md', 'Resumo – SNMP (v1)'); return false;" class="btn btn-primary">Ler Modo Visual</a>
                    </div>
                </div>
                <!-- Card 4 -->
                <div class="card">
                    <h4>Resumo – SNMPv2</h4>
                    <p>Evolução, novas operações (GetBulk, Inform), códigos de erro ampliados e boas práticas.</p>
                    <div class="btn-group">
                        <a href="resumo_snmpv2.md" target="_blank" class="btn btn-secondary">Ver Arquivo Original</a>
                        <a href="#" onclick="openModal('resumo_snmpv2.md', 'Resumo – SNMPv2'); return false;" class="btn btn-primary">Ler Modo Visual</a>
                    </div>
                </div>
                <!-- Card 5 -->
                <div class="card">
                    <h4>Resumo – SNMPv3</h4>
                    <p>Arquitetura modular, USM (auth/priv), VACM (controle de acesso) e comparação com versões anteriores.</p>
                    <div class="btn-group">
                        <a href="resumo_snmpv3.md" target="_blank" class="btn btn-secondary">Ver Arquivo Original</a>
                        <a href="#" onclick="openModal('resumo_snmpv3.md', 'Resumo – SNMPv3'); return false;" class="btn btn-primary">Ler Modo Visual</a>
                    </div>
                </div>
                <!-- Card 6 -->
                <div class="card">
                    <h4>Exercícios SNMP</h4>
                    <p>Lista de 10 informações gerenciáveis de um router Cisco ISR 4321 e mapeamento FCAPS.</p>
                    <div class="btn-group">
                        <a href="exercicios_snmp.md" target="_blank" class="btn btn-secondary">Ver Arquivo Original</a>
                        <a href="#" onclick="openModal('exercicios_snmp.md', 'Exercícios SNMP'); return false;" class="btn btn-primary">Ler Modo Visual</a>
                    </div>
                </div>
            </div>
        </section>

        <!-- Seção de Segurança -->
        <section id="seguranca">
            <h2>🛡️ Segurança de Redes</h2>
            <div class="grid-container">
                <!-- Card 1 -->
                <div class="card">
                    <h4>Introdução à Segurança</h4>
                    <p>Conceitos básicos (Ativos, Ameaças, Vulnerabilidades), Tríade CIA e tipos de ataques.</p>
                    <div class="btn-group">
                        <a href="resumo_seguranca_introducao.md" target="_blank" class="btn btn-secondary">Ver Arquivo Original</a>
                        <a href="#" onclick="openModal('resumo_seguranca_introducao.md', 'Introdução à Segurança'); return false;" class="btn btn-primary">Ler Modo Visual</a>
                    </div>
                </div>
                <!-- Card 2 -->
                <div class="card">
                    <h4>Segurança em Camadas</h4>
                    <p>Vulnerabilidades e mitigações da Camada Física (L1) até a Aplicação (L7). Firewalls e IDS/IPS.</p>
                    <div class="btn-group">
                        <a href="resumo_seguranca_redes_camadas.md" target="_blank" class="btn btn-secondary">Ver Arquivo Original</a>
                        <a href="#" onclick="openModal('resumo_seguranca_redes_camadas.md', 'Segurança em Camadas'); return false;" class="btn btn-primary">Ler Modo Visual</a>
                    </div>
                </div>
                <!-- Card 3 -->
                <div class="card">
                    <h4>Vulnerabilidades e Ataques</h4>
                    <p>Engenharia Social, Spoofing (ARP, IP, DNS), DoS/DDoS e ataques de fragmentação.</p>
                    <div class="btn-group">
                        <a href="resumo_vulnerabilidades_ataques.md" target="_blank" class="btn btn-secondary">Ver Arquivo Original</a>
                        <a href="#" onclick="openModal('resumo_vulnerabilidades_ataques.md', 'Vulnerabilidades e Ataques'); return false;" class="btn btn-primary">Ler Modo Visual</a>
                    </div>
                </div>
                <!-- Card 4 -->
                <div class="card">
                    <h4>Proteção e Defesa</h4>
                    <p>Técnicas de descoberta (Scan, Pentest), Firewalls (NGFW, Proxy), VPNs e Criptografia.</p>
                    <div class="btn-group">
                        <a href="resumo_protecao_vulnerabilidades.md" target="_blank" class="btn btn-secondary">Ver Arquivo Original</a>
                        <a href="#" onclick="openModal('resumo_protecao_vulnerabilidades.md', 'Proteção e Defesa'); return false;" class="btn btn-primary">Ler Modo Visual</a>
                    </div>
                </div>
                <!-- Card 5 -->
                <div class="card">
                    <h4>Caso NotPetya (WIRED)</h4>
                    <p>Resumo do ataque cibernético mais devastador da história e o colapso da Maersk.</p>
                    <div class="btn-group">
                        <a href="resumo_notpetya_wired.md" target="_blank" class="btn btn-secondary">Ver Arquivo Original</a>
                        <a href="#" onclick="openModal('resumo_notpetya_wired.md', 'Caso NotPetya'); return false;" class="btn btn-primary">Ler Modo Visual</a>
                    </div>
                </div>
                <!-- Card 6 -->
                <div class="card">
                    <h4>Exercícios CERT.br</h4>
                    <p>Análise estatística de incidentes no Brasil (2025): Portas visadas, Phishing e Amplificação.</p>
                    <div class="btn-group">
                        <a href="exercicios_cert_br.md" target="_blank" class="btn btn-secondary">Ver Arquivo Original</a>
                        <a href="#" onclick="openModal('exercicios_cert_br.md', 'Exercícios CERT.br'); return false;" class="btn btn-primary">Ler Modo Visual</a>
                    </div>
                </div>
                <!-- Card 7 -->
                <div class="card">
                    <h4>Exercícios Práticos</h4>
                    <p>Guia prático de ataques (Smurf, ARP Spoofing) e defesa (Nmap, Hash, GPG) para laboratório.</p>
                    <div class="btn-group">
                        <a href="exercicios_praticos_seguranca.md" target="_blank" class="btn btn-secondary">Ver Arquivo Original</a>
                        <a href="#" onclick="openModal('exercicios_praticos_seguranca.md', 'Exercícios Práticos'); return false;" class="btn btn-primary">Ler Modo Visual</a>
                    </div>
                </div>
            </div>
        </section>
    </main>

    <!-- Modal para Visualização Bonita -->
    <div id="contentModal" class="modal">
        <div class="modal-content">
            <div class="modal-header">
                <h2 id="modalTitle">Título do Documento</h2>
                <span class="close" onclick="closeModal()">&times;</span>
            </div>
            <div class="modal-body" id="modalBody">
                <!-- Conteúdo Markdown renderizado será inserido aqui -->
            </div>
        </div>
    </div>

    <footer>
        <p>Gerado por Antigravity – Assistente de Codificação Avançada.</p>
        <p>© 2025 – Material de Estudo para Redes Avançadas.</p>
    </footer>
</body>
</html>
"""

# Injetar o conteúdo JSON no template
final_html = html_template.replace('const markdownFiles = %s;', 'const markdownFiles = ' + json_content_string + ';')

# Salvar o arquivo final
with open('gerencia_redes_overview.html', 'w', encoding='utf-8') as f:
    f.write(final_html)

print("HTML gerado com sucesso com conteúdo embutido!")
