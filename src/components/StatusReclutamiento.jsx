/**
 * Barra de progreso del proceso de reclutamiento -- lo único que el
 * candidato ve de su proceso. Nunca muestra score ni clasificación.
 */

const ETAPAS_PROCESO = ['Aplicación recibida', 'En evaluación', 'Preseleccionado', 'Entrevista', 'Decisión final'];

export default function StatusReclutamiento({ status }) {
  if (status === 'Rechazado') {
    return (
      <div className="border border-[#2a2a2a] p-6 text-center">
        <p className="text-white font-semibold">Tu proceso para esta posición ha finalizado</p>
        <p className="text-[#B8BFC7] text-sm mt-1">Gracias por tu interés. Te invitamos a aplicar a futuras vacantes que encajen con tu perfil.</p>
      </div>
    );
  }

  if (status === 'Contratado') {
    return (
      <div className="border border-[#C9A14A] p-6 text-center">
        <p className="text-[#C9A14A] font-bold text-lg">¡Felicidades, fuiste seleccionado! 🎉</p>
        <p className="text-[#B8BFC7] text-sm mt-1">Pronto se pondrán en contacto contigo con los siguientes pasos.</p>
      </div>
    );
  }

  const indiceActual = ETAPAS_PROCESO.indexOf(status);

  return (
    <div className="border border-[#2a2a2a] p-6">
      <h2 className="text-sm font-semibold text-[#666] uppercase tracking-wide mb-4">¿Cómo vas en el proceso?</h2>
      <div className="flex items-center">
        {ETAPAS_PROCESO.map((etapa, i) => {
          const completada = indiceActual >= 0 && i < indiceActual;
          const actual = i === indiceActual;
          return (
            <div key={etapa} className="flex items-center flex-1 last:flex-none">
              <div className="flex flex-col items-center gap-1 text-center w-24">
                <div className={`w-7 h-7 rounded-full flex items-center justify-center text-xs font-bold ${
                  completada ? 'bg-[#0050A0] text-white' :
                  actual ? 'bg-[#D62828] text-white ring-4 ring-[#D62828]/20' :
                  'bg-[#1f1f1f] text-[#666]'
                }`}>
                  {completada ? '✓' : i + 1}
                </div>
                <span className={`text-xs ${actual ? 'font-bold text-white' : 'text-[#666]'}`}>{etapa}</span>
              </div>
              {i < ETAPAS_PROCESO.length - 1 && (
                <div className={`flex-1 h-0.5 ${completada ? 'bg-[#0050A0]' : 'bg-[#1f1f1f]'}`}></div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
