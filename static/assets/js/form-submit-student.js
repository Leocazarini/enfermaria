document.getElementById("student-submit-button").addEventListener("click", function(event) {
    event.preventDefault(); // Evita o envio padrão do formulário

    // Coletando os dados do formulário
    const studentId = document.getElementById("student-id").textContent;
    const allergies = document.getElementById("allergies").value;
    const patientNotes = document.getElementById("student-notes").value;
    const currentClass = document.getElementById("current-class").value;
    const infirmary = sessionStorage.getItem('infirmary');
    const nurse = sessionStorage.getItem('userFirstName');
    const reason = document.getElementById("reason").value;
    const treatment = document.getElementById("treatment").value;
    const notes = document.getElementById("notes").value;
    const revaluation = document.getElementById("revaluation").checked;
    const contactParents = document.getElementById("contact-parents").checked;

    // Montando o objeto de dados
    const data = {
        student_id: studentId,
        allergies: allergies,
        patient_notes: patientNotes,
        current_class: currentClass,
        infirmary: infirmary,
        nurse: nurse,
        reason: reason,
        treatment: treatment,
        notes: notes,
        revaluation: revaluation,
        contact_parents: contactParents,
        date: new Date().toISOString() // Ajuste conforme necessário para obter a data no formato desejado
    };

    // Convertendo para JSON
    const jsonData = JSON.stringify(data);

    // Enviando para o backend
    fetch("/appointments/student/record/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: jsonData
    })
    .then(response => response.json())
    .then(data => {
        console.log("Success:", data);
        // Aqui você pode adicionar lógica para tratar a resposta do backend
    })
    .catch((error) => {
        console.error("Error:", error);
        // Aqui você pode adicionar lógica para tratar erros na requisição
    });
});


