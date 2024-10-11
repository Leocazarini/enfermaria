document.getElementById("visitor-submit-button").addEventListener("click", function(event) {
    event.preventDefault(); // Evita o envio padrão do formulário

    // Coletando os dados do formulário
    const visitorId = document.getElementById("visitor-id").value;
    const visitorName = document.getElementById("name").value;
    const visitorAge = document.getElementById("age").value;
    const visitorEmail = document.getElementById("email").value;
    const visitorGender = document.getElementById("gender").value;
    const allergies = document.getElementById("allergies").value;
    const visitorRelationship = document.getElementById("relationship").value;
    const patientNotes = document.getElementById("visitor-notes").value;
    const infirmary = sessionStorage.getItem('infirmary');
    const nurse = sessionStorage.getItem('userFirstName');
    const reason = document.getElementById("reason").value;
    const treatment = document.getElementById("treatment").value;
    const notes = document.getElementById("notes").value;
    const revaluation = document.getElementById("revaluation").checked;

    

    // Montando o objeto de dados
    const data = {
        visitor_id: visitorId,
        visitor_name: visitorName,
        visitor_age: visitorAge,
        visitor_email: visitorEmail,
        visitor_gender: visitorGender,
        allergies: allergies,
        visitor_relationship: visitorRelationship,
        patient_notes: patientNotes,
        infirmary: infirmary,
        nurse: nurse,
        reason: reason,
        treatment: treatment,
        notes: notes,
        revaluation: revaluation,
        date: new Date().toISOString() // Ajuste conforme necessário para obter a data no formato desejado
    };

    // Convertendo para JSON
    const jsonData = JSON.stringify(data);


    
    // Enviando para o backend
    fetch("/appointments/visitor/record/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: jsonData
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            // Exibir um alerta de sucesso
            alert("Atendimento salvo com sucesso!");

            // Redirecionar para a página principal 
             window.location.href = "/"; 
        } else {
            alert("Ocorreu um erro ao salvar o atendimento.");
        }
    })
    .catch((error) => {
        console.error("Error:", error);
        alert("Ocorreu um erro na requisição. Por favor, tente novamente.");
    });
});

