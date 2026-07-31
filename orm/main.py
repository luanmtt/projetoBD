from datetime import datetime
from database import engine, SessionLocal, Base
import models
import CRUD
from test_cases import popular_banco


# ──────────────────────────────────────────────────────────────────────────────────────────────────


def main():
    popular_banco()

    with SessionLocal() as session:
        atendimentos = CRUD.list_atend(
            session=session, 
            nome_paciente="Akemi Almirante"
        )
        for at in atendimentos:
            print(f"ID: {at.id_atendimento} | Data: {at.data_hora} | Paciente: {at.paciente.nome}")
            
# ──────────────────────────────────────────────────────────────────────────────────────────────────
        
        print("\n" + "━"*80)
        print("1. PRECEPTORES QUE ATENDERAM PACIENTES FLAMENGUISTAS")
        print("━"*80)
        preceptores = CRUD.listar_preceptores_pacientes_flamenguistas(session)
        for p in preceptores:
            print(f"Preceptor: {p.nome} | Titulação: {p.titulacao} | CRM: {p.crm}")
        
        print("\n" + "━"*80)
        print("2. ÚLTIMO ATENDIMENTO POR PACIENTE (Testando Eager Loading)")
        print("━"*80)
        ultimos_atendimentos = CRUD.listar_ultimo_atendimento_por_paciente(session)
        for at in ultimos_atendimentos:
            print(f"\nData: {at.data_hora} | Paciente: {at.paciente.nome}")
            print(f"   Residente: {at.residente.nome}")
            print(f"   Preceptor: {at.preceptor.nome}")
            
            print(f"   Procedimentos Realizados ({len(at.procedimentos_realizados)}):")
            for pr in at.procedimentos_realizados:
                print(f"     - {pr.procedimento.nome} (Qtd: {pr.quantidade})")

        
        print("\n" + "━"*80)
        print("3. ESTATÍSTICAS DE RISCO POR RESIDENTE")
        print("━"*80)
        estatisticas = CRUD.percentual_alto_risco_por_residente(session)
        for stat in estatisticas:
           
            print(f"Residente: {stat.nome_residente}")
            print(f"   Total de procedimentos: {stat.total}")
            
            perc = stat.percentual_alto_risco or 0 
            print(f"   Taxa de Alto Risco: {perc:.2f}%\n")

# ──────────────────────────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    main()


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

