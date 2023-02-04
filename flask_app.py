from datetime import datetime, timedelta
from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        start_date_str = request.form['start_date']
        end_date_str = request.form['end_date']
        start_date = datetime.strptime(start_date_str, "%d/%m/%Y")
        end_date = datetime.strptime(end_date_str, "%d/%m/%Y")
        delta = end_date - start_date
        total_days = delta.days + 1
        weekends = (total_days // 7) * 2
        if (total_days % 7 == 5):
            weekends += 1
        elif (total_days % 7 == 6):
            weekends += 2
        work_days = total_days - weekends
        daySubMatrix = [[1, 1, 1, 1, 0, 0],
                        [1, 1, 1, 1, 0, 0],
                        [1, 1, 1, 1, 2, 1],
                        [0, 0, 1, 1, 1, 1],
                        [1, 1, 0, 0, 1, 1]]
        att_per = [0, 0, 0, 0, 0, 0]
        tot_per = [0, 0, 0, 0, 0, 0]
        holidays = [0, 0, 0, 0, 0]
        absent_days = [0, 0, 0, 0, 0]
        weekdays = ['Wednesday', 'Thursday', 'Friday', 'Saturday', 'Tuesday']
        
        for i, day in enumerate(weekdays):
            day = request.form[f"{day}_absent"]
            absent_days[i] = int(day)
        for i, day in enumerate(weekdays):
            day = request.form[f"{day}_holiday"]
            holidays[i] = int(day)
        percent = [0, 0, 0, 0, 0, 0]
        leaves = [absent_days[i] + holidays[i] for i in range(5)]
        for i in range(work_days):
            x = i % 5
            if (holidays[x] > 0):
                holidays[x] -= 1
                continue
            for j in range(6):
                tot_per[j] += daySubMatrix[x][j]
        for i in range(work_days):
            x = i % 5
            if (leaves[x] > 0):
                leaves[x] -= 1
                continue
            for j in range(6):
                att_per[j] += daySubMatrix[x][j]
        for i in range(6):
            percent[i] = round((att_per[i] / tot_per[i]) * 100,2)
        return render_template('result.html', percent=percent)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=False)
