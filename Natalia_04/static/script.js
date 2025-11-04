// Início do namoro (YYYY, M-1, D, H, M, S)
const inicio = new Date(2025, 2, 4, 0, 0, 0); // 04/03/2025 - meses JavaScript começam em 0

function diffFull(start, now) {
    let y = now.getFullYear() - start.getFullYear();
    let m = now.getMonth() - start.getMonth();
    let d = now.getDate() - start.getDate();
    let H = now.getHours() - start.getHours();
    let Min = now.getMinutes() - start.getMinutes();

    if (Min < 0) { Min += 60; H -= 1; }
    if (H < 0) { H += 24; d -= 1; }

    if (d < 0) {
        // dias do mês anterior ao 'now'
        const prevMonth = new Date(now.getFullYear(), now.getMonth(), 0);
        d += prevMonth.getDate();
        m -= 1;
    }
    if (m < 0) {
        m += 12;
        y -= 1;
    }
    if (y < 0) {
        // caso a data inicial seja no futuro (não deve)
        y = 0; m = 0; d = 0; H = 0; Min = 0;
    }

    return { years: y, months: m, days: d, hours: H, minutes: Min };
}

function atualizar() {
    const agora = new Date();
    const diff = diffFull(inicio, agora);
    let texto = `${diff.years} anos, ${diff.months} meses, ${diff.days} dias, ${diff.hours} horas e ${diff.minutes} minutos`;
    document.getElementById('contador-text').innerText = texto;
}

setInterval(atualizar, 1000);
atualizar();
