<!DOCTYPE html>
<html>
<head>
    <title>Mon Quiz Privé</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: sans-serif; text-align: center; background: #f0f2f5; padding: 20px; }
        .card { background: white; padding: 20px; border-radius: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); max-width: 500px; margin: auto; }
        button { background: #007bff; color: white; border: none; padding: 10px 20px; margin: 10px; border-radius: 5px; cursor: pointer; width: 80%; }
        button:hover { background: #0056b3; }
        #result { font-weight: bold; margin-top: 20px; color: green; }
    </style>
</head>
<body>
    <div class="card">
        <h2 id="question">Chargement du quiz...</h2>
        <div id="options"></div>
        <p id="result"></p>
        <p>Score : <span id="score">0</span></p>
    </div>

    <script>
        const questions = [
            { q: "Quelle est la capitale de la France ?", a: ["Lyon", "Paris", "Marseille"], correct: 1 },
            { q: "Qui a peint la Joconde ?", a: ["Picasso", "Van Gogh", "De Vinci"], correct: 2 },
            { q: "Combien font 7 x 8 ?", a: ["54", "56", "64"], correct: 1 }
        ];

        let currentQ = 0;
        let score = 0;

        function loadQuestion() {
            const q = questions[currentQ];
            document.getElementById("question").innerText = q.q;
            const optionsDiv = document.getElementById("options");
            optionsDiv.innerHTML = "";
            q.a.forEach((opt, i) => {
                const btn = document.createElement("button");
                btn.innerText = opt;
                btn.onclick = () => checkAnswer(i);
                optionsDiv.appendChild(btn);
            });
        }

        function checkAnswer(i) {
            if(i === questions[currentQ].correct) {
                score++;
                document.getElementById("result").innerText = "Bravo ! ✅";
            } else {
                document.getElementById("result").innerText = "Raté... ❌";
            }
            document.getElementById("score").innerText = score;
            currentQ++;
            if(currentQ < questions.length) {
                setTimeout(() => {
                    document.getElementById("result").innerText = "";
                    loadQuestion();
                }, 1000);
            } else {
                document.getElementById("card").innerHTML = "<h1>Fini ! Score final : " + score + "/" + questions.length + "</h1>";
            }
        }
        loadQuestion();
    </script>
</body>
</html>
