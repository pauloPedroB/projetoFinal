import mysql.connector


db = mysql.connector.connect(
    host="localhost",
    user="aluno",
    password="toor",
    database="projetoAutomoveis"
)
cursor = db.cursor()
cursor.execute("INSERT INTO produtos (nome_produto, categoria, img) VALUES "
"('Troca de óleo e filtro', 'Manutenção Geral', 'https://atrialub.com.br/wp-content/uploads/2018/11/catalogo_fundo_lust.jpg'),"
"('Troca de fluidos (arrefecimento, transmissão, freio)', 'Manutenção Geral', 'https://cpfabbri.com.br/wp-content/uploads/2023/11/fluidos-de-carro-quais-sao-os-diferentes-tipos-quando-trocar-oficina.png'),"
"('Substituição de velas de ignição e cabos', 'Manutenção Geral', 'https://www.azulseguros.com.br/wp-content/uploads/2013/11/skd282543sdc.jpg'),"
"('Inspeção de correias e tensionadores', 'Manutenção Geral', 'https://www.azulseguros.com.br/wp-content/uploads/2014/03/correias.jpg'),"
"('Revisão de sistemas elétricos e eletrônicos', 'Manutenção Geral', 'https://kmctecnologia.com/wp-content/uploads/2023/06/248-as-pricipais-manutencoes-no-sistema-eletrico-e-eletronico-do-carro.png'),"

"('Reparação de motor e transmissão', 'Reparação Mecânica', 'https://st3.depositphotos.com/2165825/34633/i/1600/depositphotos_346331552-stock-photo-car-repair-type-of-open.jpg'),"
"('Substituição de componentes defeituosos (alternador, bomba d’água, etc.)', 'Reparação Mecânica', 'https://minhaoficina.net/wp-content/uploads/2016/07/alternador-e1544785190113.jpg'),"
"('Reparação de sistemas de suspensão e direção', 'Reparação Mecânica', 'https://cdn.appdealersites.com.br/bamaq/suspensao-automotiva.jpg'),"
"('Substituição de embreagem', 'Reparação Mecânica', 'https://blog.karvi.com.br/wp-content/uploads/2022/11/caixa-de-transmiss%C3%A3o-e-pedais-do-carro.png'),"
"('Reparação de sistemas de freio', 'Reparação Mecânica', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQbIfIVDF3VeUQjMaj4HmHnc9mImqpuyHsKSA&s'),"

"('Diagnóstico e reparação de problemas elétricos', 'Sistemas Elétricos e Eletrônicos', 'https://autopecaspingodouro.com.br/wp-content/uploads/2022/12/parte-eletrica-do-carro-1.jpg'),"
"('Instalação e reparação de sistemas de iluminação', 'Sistemas Elétricos e Eletrônicos', 'https://energycar.com.br/wp-content/uploads/2021/11/Lampadas_1.jpg'),"
"('Instalação de sistemas de som e multimídia', 'Sistemas Elétricos e Eletrônicos', 'https://liderautoacessorios.com.br/wp-content/uploads/2019/10/Central-Multimidia-Android-3.jpg'),"

"('Manutenção e recarga de sistemas de ar-condicionado', 'Sistemas de Ar-Condicionado e Refrigeração', 'https://europneussp.com.br/wp-content/uploads/2023/07/manutencao-e-recarga-de-ar-condicionado.jpg'),"
"('Reparação de sistemas de arrefecimento', 'Sistemas de Ar-Condicionado e Refrigeração', 'https://www.minutoseguros.com.br/blog/wp-content/uploads/2019/02/sistema-de-arrefecimento-2.jpg'),"

"('Alinhamento de rodas', 'Alinhamento e Balanceamento', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS2qjKmeg829KpHLQNWvnCwiTteU3LiY_l9dw&s'),"
"('Balanceamento de pneus e rodas', 'Alinhamento e Balanceamento', 'https://griffepneus.com.br/wp-content/uploads/2022/02/alinhamento-e-balanceamento-07-e1645298890680.jpg'),"

"('Uso de scanners automotivos para identificar problemas', 'Diagnóstico por Computador', 'https://site.jairoleos.com.br/wp-content/uploads/2019/02/Scanner-automotivo-capa-763x445-1.jpg'),"
"('Leitura e redefinição de códigos de erro (check engine)', 'Diagnóstico por Computador', 'https://m.media-amazon.com/images/I/81DqpXF7ZuL.jpg'),"

"('Inspeção veicular', 'Inspeção e Emissão de Certificados', 'https://localizafrotas-prd.azurewebsites.net/wp-content/uploads/mecanico-fazendo-inspecao-do-carro.jpg.webp'),"
"('Emissão de certificados de inspeção', 'Inspeção e Emissão de Certificados', 'https://localizafrotas-prd.azurewebsites.net/wp-content/uploads/mecanico-fazendo-inspecao-do-carro.jpg.webp'),"

"('Instalação de kits de elevação/rebaixamento', 'Personalização e Modificações', 'https://preview.redd.it/h-r-45mm-lowering-cup-kit-for-jimny-v0-6srp9rul95id1.jpg?width=2016&format=pjpg&auto=webp&s=77b3acbc5f5f9f8596b3e14c3079b277276b64ca'),"
"('Personalização de rodas e pneus', 'Personalização e Modificações', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT4WchI94yadABBWkGSXPcBudebNDMuRUX1sw&s'),"
"('Instalação de acessórios (barras de tejadilho, suportes, etc.)', 'Personalização e Modificações', 'https://m.media-amazon.com/images/I/61ymBAYGXwL._AC_UF1000,1000_QL80_.jpg'),"

"('Reparação de amassados e arranhões', 'Soldagem e Reparação de Carroceria', 'https://neycostaautocenter.com.br/wp-content/uploads/2024/11/18102.jpg'),"
"('Soldagem de partes estruturais', 'Soldagem e Reparação de Carroceria', 'https://projetandohoje.com.br/wdadmin/uploads/blog_postagens/a-importancia-da-soldagem-em-estruturas-metalicas-202303131014.jpg'),"

"('Troca de pastilhas e discos de freio', 'Manutenção de Freio', 'https://blog.fras-le.com/wp-content/uploads/2018/10/245242-especialista-responde-qual-o-momento-para-trocar-pastilha-de-freio.jpg'),"
"('Sangria do sistema de freio', 'Manutenção de Freio', 'https://blog.fras-le.com/wp-content/uploads/2018/10/245242-especialista-responde-qual-o-momento-para-trocar-pastilha-de-freio.jpg'),"
"('Substituição de amortecedores e molas', 'Manutenção de Suspensão', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQlKr9tRMdKg1KH2uggOAA7OQo-zPDdTIcG6g&s')"
)
db.commit()