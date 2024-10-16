document.getElementById("employee-submit-button").addEventListener("click", function(event) {
    event.preventDefault(); // Evita o envio padrão do formulário
    console.log("Button clicked, preparing to send data...");

    // Coletando os dados do formulário
    const employeeId = document.getElementById("employee-id").textContent;
    const allergies = document.getElementById("allergies").value;
    const patientNotes = document.getElementById("employee-notes").value;
    const infirmary = sessionStorage.getItem('infirmary');
    const nurse = sessionStorage.getItem('userFirstName');
    const reason = document.getElementById("reason").value;
    const treatment = document.getElementById("treatment").value;
    const notes = document.getElementById("notes").value;
    const revaluation = document.getElementById("revaluation").checked;


    // Montando o objeto de dados
    const data = {
        employee_id: employeeId,
        allergies: allergies,
        patient_notes: patientNotes,
        infirmary: infirmary,
        nurse: nurse,
        reason: reason,
        treatment: treatment,
        notes: notes,
        revaluation: revaluation,
        // date: new Date().toISOString() 
    };

    // Convertendo para JSON
    const jsonData = JSON.stringify(data);
    console.log("Data prepared:", jsonData);

    // Enviando para o backend
    fetch("/appointments/employee/record/", {
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