#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re

# Ler o arquivo
with open('index copy.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Adicionar jsPDF no head
if 'jspdf.umd.min.js' not in content:
    content = content.replace('    </style>\n</head>', 
                              '    </style>\n    <!-- jsPDF library for PDF generation -->\n    <script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js"></script>\n</head>')

# 2. Atualizar URL do webhook
content = re.sub(r"https://hook\.us1\.make\.com/[^\']+", 
                 "https://n8n.sparkleads.pro/webhook/d877abb2-4d6f-464f-9b55-30249a7f2892", 
                 content)

# 3. Adicionar função generatePDF antes de sendToWebhook
if 'function generatePDF' not in content:
    pdf_function = '''            }
            
            // Função para gerar PDF com todas as respostas do formulário
            function generatePDF(webhookData) {
                const { jsPDF } = window.jspdf;
                const doc = new jsPDF();
                
                let yPos = 20;
                const pageHeight = doc.internal.pageSize.height;
                const margin = 20;
                const lineHeight = 7;
                const maxWidth = 170;
                
                // Título
                doc.setFontSize(18);
                doc.setFont(undefined, 'bold');
                doc.text('Formulário de Cadastro - Respostas', margin, yPos);
                yPos += 15;
                
                // Função auxiliar para adicionar texto com quebra de linha
                function addText(label, value, isBold = false) {
                    if (yPos > pageHeight - 30) {
                        doc.addPage();
                        yPos = 20;
                    }
                    
                    doc.setFontSize(10);
                    doc.setFont(undefined, isBold ? 'bold' : 'normal');
                    
                    const labelText = label + ':';
                    doc.text(labelText, margin, yPos);
                    
                    if (value && value.toString().trim() !== '') {
                        const valueText = value.toString();
                        const lines = doc.splitTextToSize(valueText, maxWidth);
                        doc.setFont(undefined, 'normal');
                        doc.text(lines, margin + 5, yPos + lineHeight);
                        yPos += (lines.length * lineHeight) + 5;
                    } else {
                        doc.setFont(undefined, 'normal');
                        doc.text('Não informado', margin + 5, yPos + lineHeight);
                        yPos += lineHeight + 5;
                    }
                }
                
                // Informações Pessoais
                doc.setFontSize(14);
                doc.setFont(undefined, 'bold');
                doc.text('INFORMAÇÕES PESSOAIS', margin, yPos);
                yPos += 10;
                
                addText('Nome Completo', webhookData.full_name, true);
                addText('Email', webhookData.email);
                addText('Telefone', webhookData.phone);
                addText('Profissão', webhookData.profession);
                addText('Data de Nascimento', webhookData.dateOfBirth);
                addText('Status de Documentação', webhookData.documentation_status);
                addText('Há quanto tempo está nos EUA?', webhookData.time_in_usa);
                addText('Onde morava no Brasil?', webhookData.previous_city_brazil);
                addText('Trabalhava com o que no Brasil?', webhookData.previous_profession_brazil);
                
                // Informações do Cônjuge
                yPos += 5;
                doc.setFontSize(14);
                doc.setFont(undefined, 'bold');
                doc.text('INFORMAÇÕES DO CÔNJUGE', margin, yPos);
                yPos += 10;
                
                addText('Possui Cônjuge?', webhookData.has_spouse);
                addText('Nome do Cônjuge', webhookData.spouse_name);
                addText('Data de Nascimento do Cônjuge', webhookData.spouse_birthdate);
                addText('Profissão do Cônjuge', webhookData.spouse_profession);
                addText('Comentários sobre o Cônjuge', webhookData.spouse_comments);
                
                // Informações dos Filhos
                yPos += 5;
                doc.setFontSize(14);
                doc.setFont(undefined, 'bold');
                doc.text('INFORMAÇÕES DOS FILHOS', margin, yPos);
                yPos += 10;
                
                addText('Possui Filhos?', webhookData.has_children);
                addText('Quantidade de Filhos', webhookData.children_count);
                
                // Adicionar informações de cada filho
                if (webhookData.children && Array.isArray(webhookData.children)) {
                    webhookData.children.forEach((child, index) => {
                        yPos += 3;
                        doc.setFontSize(12);
                        doc.setFont(undefined, 'bold');
                        doc.text(\`Filho \${index + 1}\`, margin, yPos);
                        yPos += 7;
                        addText('Nome', child.name);
                        addText('Data de Nascimento', child.birthdate);
                        addText('Comentários', child.comments);
                    });
                }
                
                // Informações Financeiras
                yPos += 5;
                doc.setFontSize(14);
                doc.setFont(undefined, 'bold');
                doc.text('INFORMAÇÕES FINANCEIRAS', margin, yPos);
                yPos += 10;
                
                addText('Possui algum seguro?', webhookData.has_insurance);
                addText('Tipo de seguro', webhookData.insurance_type);
                addText('Cobertura atual', webhookData.insurance_coverage);
                addText('Possui Aposentadoria?', webhookData.has_retirement);
                addText('Tipos de Aposentadoria', webhookData.retirement_types);
                addText('O que é mais importante para você?', webhookData.priority);
                addText('Quem gera mais Renda na casa?', webhookData.income_generator);
                addText('Percentual do Cliente (%)', webhookData.client_income_percentage);
                addText('Percentual do Cônjuge (%)', webhookData.spouse_income_percentage);
                addText('Possui investimento?', webhookData.has_investment);
                addText('Tipo de investimento', webhookData.investment_type);
                addText('Valor do investimento', webhookData.investment_value);
                addText('Tempo de sobrevivência', webhookData.survival_time);
                addText('Status da casa', webhookData.house_status);
                addText('Possui hipoteca?', webhookData.has_mortgage);
                addText('Valor da hipoteca', webhookData.mortgage_value);
                addText('Despesa mensal', webhookData.monthly_expense);
                addText('Renda mensal', webhookData.monthly_income);
                
                if (webhookData.meeting_comments) {
                    addText('Comentários da reunião', webhookData.meeting_comments);
                }
                
                // Data e hora de geração
                yPos += 10;
                doc.setFontSize(8);
                doc.setFont(undefined, 'italic');
                const now = new Date();
                const dateStr = now.toLocaleString('pt-BR');
                doc.text(\`Gerado em: \${dateStr}\`, margin, yPos);
                
                return doc;
            }
            
            // Enviar dados para webhook com melhor tratamento de erros'''
    
    # Encontrar onde inserir (antes de sendToWebhook)
    pattern = r'(            }\s*\n\s*// Enviar dados para webhook com melhor tratamento de erros)'
    content = re.sub(pattern, pdf_function, content)

# 4. Modificar sendToWebhook para enviar PDF
old_fetch = r"console\.log\('Enviando dados para webhook:', JSON\.stringify\(webhookData\)\);\s*\n\s*// Adicionar timeout para a requisição\s*\n\s*const controller = new AbortController\(\);\s*const timeoutId = setTimeout\(\(\) => controller\.abort\(\), 30000\); // 30 segundos timeout\s*\n\s*const response = await fetch\(webhookUrl, \{\s*method: 'POST',\s*headers: \{\s*'Content-Type': 'application/json',\s*'Accept': 'application/json'\s*\},\s*body: JSON\.stringify\(webhookData\),\s*signal: controller\.signal\s*\}\)\.finally\(\(\) => clearTimeout\(timeoutId\)\);"

new_fetch = """console.log('Enviando dados para webhook:', JSON.stringify(webhookData));
                    
                    // Gerar PDF com todas as respostas
                    const pdfDoc = generatePDF(webhookData);
                    const pdfBlob = pdfDoc.output('blob');
                    
                    // Criar FormData para enviar JSON e PDF
                    const formData = new FormData();
                    formData.append('data', JSON.stringify(webhookData));
                    formData.append('pdf', pdfBlob, 'formulario_respostas.pdf');
                    
                    // Adicionar timeout para a requisição
                    const controller = new AbortController();
                    const timeoutId = setTimeout(() => controller.abort(), 30000); // 30 segundos timeout
                    
                    const response = await fetch(webhookUrl, {
                        method: 'POST',
                        body: formData,
                        signal: controller.signal
                    }).finally(() => clearTimeout(timeoutId));"""

content = re.sub(old_fetch, new_fetch, content, flags=re.MULTILINE | re.DOTALL)

# Salvar o arquivo
with open('index copy.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('Todas as modificações foram aplicadas com sucesso!')
print('- Biblioteca jsPDF adicionada')
print('- URL do webhook atualizada')
print('- Função generatePDF adicionada')
print('- Função sendToWebhook modificada para enviar PDF')

