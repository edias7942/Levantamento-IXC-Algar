import ProgressBar from 'progress';

// Função que simula uma tarefa assíncrona com atraso
function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function simulateTask() {
  // Configuração da barra de progresso
  const total = 360;  // Total de 100% de progresso
  const bar = new ProgressBar('  processing [:bar] :percent :current/:total', {
    total: total,
    width: 100,
    complete: '=',
    incomplete: '',
  });

  // Simulando uma tarefa assíncrona com um delay
  for (let i = 0; i < total; i++) {
    await sleep(100);  // Espera 100ms antes de avançar no progresso
    bar.tick();  // Avança a barra de progresso
  }

  console.log('\nTask completed!');
}

simulateTask();
