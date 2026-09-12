from flask import Flask, request, render_template_string
from Bio import SeqIO
from io import StringIO

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>FASTA File Parser</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 900px;
            margin: 40px auto;
            padding: 20px;
        }

        h1 {
            text-align: center;
        }

        .box {
            border: 1px solid #ddd;
            padding: 25px;
            border-radius: 10px;
            margin-top: 20px;
        }

        button {
            padding: 10px 20px;
            cursor: pointer;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }

        th, td {
            border: 1px solid #ddd;
            padding: 10px;
            text-align: left;
        }

        th {
            background: #f2f2f2;
        }

        .error {
            color: red;
            margin-top: 20px;
        }
    </style>
</head>

<body>

<h1>🧬 FASTA File Parser</h1>

<div class="box">

<form method="POST" enctype="multipart/form-data">

    <label>Select a FASTA file:</label>
    <br><br>

    <input type="file" name="fasta_file" accept=".fasta,.fa,.fna" required>

    <br><br>

    <button type="submit">Parse FASTA</button>

</form>

{% if results %}

<h2>Results</h2>

<table>

<tr>
    <th>Sequence ID</th>
    <th>Length (bp)</th>
    <th>GC Content (%)</th>
</tr>

{% for result in results %}

<tr>
    <td>{{ result.id }}</td>
    <td>{{ result.length }}</td>
    <td>{{ "%.2f"|format(result.gc) }}</td>
</tr>

{% endfor %}

</table>

{% endif %}

{% if error %}

<p class="error">{{ error }}</p>

{% endif %}

</div>

</body>
</html>
"""


def calculate_gc_content(sequence):
    """Calculate GC content percentage of a DNA sequence."""

    sequence = str(sequence).upper()

    if len(sequence) == 0:
        return 0.0

    gc_count = sequence.count("G") + sequence.count("C")

    return (gc_count / len(sequence)) * 100


@app.route("/", methods=["GET", "POST"])
def home():

    results = []
    error = None

    if request.method == "POST":

        file = request.files.get("fasta_file")

        if not file or file.filename == "":
            error = "Please select a FASTA file."
            return render_template_string(
                HTML,
                results=results,
                error=error
            )

        try:

            content = file.read().decode("utf-8")

            records = SeqIO.parse(
                StringIO(content),
                "fasta"
            )

            for record in records:

                sequence = record.seq

                results.append({
                    "id": record.id,
                    "length": len(sequence),
                    "gc": calculate_gc_content(sequence)
                })

        except Exception as e:

            error = f"Error parsing FASTA file: {str(e)}"

    return render_template_string(
        HTML,
        results=results,
        error=error
    )


if __name__ == "__main__":
    app.run(debug=True)