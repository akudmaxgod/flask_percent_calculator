from flask import Flask, render_template, request

app = Flask(__name__)

USD_TO_UAH = 40.25
calc_totals = {1: None, 2: None, 3: None}
histories = {1: [], 2: [], 3: []}
calc3_input_string = ""  # <- добавили

@app.route('/', methods=['GET', 'POST'])
def index():
    global calc_totals, histories, calc3_input_string

    if request.method == 'POST':
        calc_id = int(request.form.get('calc_id'))
        values_raw = request.form.get(f'values{calc_id}', '').strip()

        try:
            numbers = [float(x.strip().replace(',', '.')) for x in values_raw.split('+') if x.strip()]
            if not numbers:
                raise ValueError("Пустой ввод")

            if calc_id in [1, 2]:
                total = round(sum(x * 0.87 for x in numbers), 2)
            else:
                total = round(sum(numbers), 2)

            usd_value = round(total / USD_TO_UAH, 2)
            calc_totals[calc_id] = (total, usd_value)

            entry = f"{'+'.join(map(str, numbers))} → {total} ₴ ({usd_value} $)"
            histories[calc_id].insert(0, entry)
            histories[calc_id] = histories[calc_id][:5]

            # Новая логика — добавляем в строку калькулятора 3
            if calc_id == 1:
                if calc3_input_string:
                    calc3_input_string += f"+{total}"
                else:
                    calc3_input_string = f"{total}"

        except Exception as e:
            print("Ошибка обработки ввода:", e)

    return render_template(
        'index.html',
        calc_totals=calc_totals,
        histories=histories,
        usd_to_uah=USD_TO_UAH,
        calc3_input_string=calc3_input_string  # <- передаём в шаблон
    )

if __name__ == '__main__':
    app.run(debug=True)
