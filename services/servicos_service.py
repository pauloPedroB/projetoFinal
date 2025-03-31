import mysql.connector


db = mysql.connector.connect(
    host="localhost",
    user="aluno",
    password="toor",
    database="projetoAutomoveis"
)
cursor = db.cursor()
cursor.execute("INSERT INTO produtos (nome_produto, categoria, img) VALUES "
"('Troca de óleo e filtro', 'Manutenção Geral', 'https://example.com/troca_oleo.jpg'),"
"('Troca de fluidos (arrefecimento, transmissão, freio)', 'Manutenção Geral', 'https://example.com/troca_fluidos.jpg'),('Substituição de velas de ignição e cabos', 'Manutenção Geral', 'https://example.com/velas_ignicao.jpg'),"
"('Inspeção de correias e tensionadores', 'Manutenção Geral', 'https://example.com/correias_tensionadores.jpg'),"
"('Revisão de sistemas elétricos e eletrônicos', 'Manutenção Geral', 'https://example.com/sistemas_eletricos.jpg'),"

"('Reparação de motor e transmissão', 'Reparação Mecânica', 'https://example.com/motor_transmissao.jpg'),"
"('Substituição de componentes defeituosos (alternador, bomba d’água, etc.)', 'Reparação Mecânica', 'https://example.com/componentes_defeituosos.jpg'),"
"('Reparação de sistemas de suspensão e direção', 'Reparação Mecânica', 'https://example.com/suspensao_direcao.jpg'),"
"('Substituição de embreagem', 'Reparação Mecânica', 'https://example.com/embreagem.jpg'),"
"('Reparação de sistemas de freio', 'Reparação Mecânica', 'https://example.com/sistemas_freio.jpg'),"

"('Diagnóstico e reparação de problemas elétricos', 'Sistemas Elétricos e Eletrônicos', 'https://example.com/diagnostico_eletrico.jpg'),"
"('Instalação e reparação de sistemas de iluminação', 'Sistemas Elétricos e Eletrônicos', 'https://example.com/sistemas_iluminacao.jpg'),"
"('Instalação de sistemas de som e multimídia', 'Sistemas Elétricos e Eletrônicos', 'https://example.com/som_multimidia.jpg'),"

"('Manutenção e recarga de sistemas de ar-condicionado', 'Sistemas de Ar-Condicionado e Refrigeração', 'https://example.com/ar_condicionado.jpg'),"
"('Reparação de sistemas de arrefecimento', 'Sistemas de Ar-Condicionado e Refrigeração', 'https://example.com/sistema_arrefecimento.jpg'),"

"('Alinhamento de rodas', 'Alinhamento e Balanceamento', 'https://example.com/alinhamento_rodas.jpg'),"
"('Balanceamento de pneus e rodas', 'Alinhamento e Balanceamento', 'https://example.com/balanceamento_pneus.jpg'),"

"('Uso de scanners automotivos para identificar problemas', 'Diagnóstico por Computador', 'https://example.com/scanner_automotivo.jpg'),"
"('Leitura e redefinição de códigos de erro (check engine)', 'Diagnóstico por Computador', 'https://example.com/check_engine.jpg'),"

"('Inspeção veicular', 'Inspeção e Emissão de Certificados', 'https://example.com/inspecao_veicular.jpg'),"
"('Emissão de certificados de inspeção', 'Inspeção e Emissão de Certificados', 'https://example.com/certificado_inspecao.jpg'),"

"('Instalação de kits de elevação/rebaixamento', 'Personalização e Modificações', 'https://example.com/kits_elevacao.jpg'),"
"('Personalização de rodas e pneus', 'Personalização e Modificações', 'https://example.com/rodas_pneus.jpg'),"
"('Instalação de acessórios (barras de tejadilho, suportes, etc.)', 'Personalização e Modificações', 'https://example.com/acessorios_carro.jpg'),"

"('Reparação de amassados e arranhões', 'Soldagem e Reparação de Carroceria', 'https://example.com/amassados_arranhoes.jpg'),"
"('Soldagem de partes estruturais', 'Soldagem e Reparação de Carroceria', 'https://example.com/soldagem_estrutural.jpg'),"

"('Troca de pastilhas e discos de freio', 'Manutenção de Freio', 'https://example.com/pastilhas_disco_freio.jpg'),"
"('Sangria do sistema de freio', 'Manutenção de Freio', 'https://example.com/sangria_freio.jpg'),"
"('Substituição de amortecedores e molas', 'Manutenção de Suspensão', 'https://example.com/amortecedores_molas.jpg')"
)
db.commit()