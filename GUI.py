from customtkinter import CTk, CTkLabel
from customtkinter import *
from Logistic.Logic import algoritmo_gen
from Logistic.Logic import crear_video

# CTk.set_appearance_mode("Dark")

class MiVentana(CTk):
    button_a_enabled = True
    button_b_enabled = True

    def __init__(self):
        super().__init__()

        self.title("Algoritmos Genéticos")
        self.geometry("750x550")
        self.resizable(False, False)

        # CONFIGURACIÓN PRINCIPAL
        self.labelGeneraciones = CTkLabel(self, text="GENERACIONES", text_color="#3CC0C9")
        self.labelGeneraciones.place(x=40, y=20)
        self.labelGeneraciones.configure(font=("TkDefaultFont", 24, "bold"), text_color="#FFA500")

        self.labelFx = CTkLabel(self, text="f(x):", text_color="#fff")
        self.labelFx.place(x=50, y=70)
        self.labelFx.configure(font=("TkDefaultFont", 12, "bold"))

        self.entradaFx = CTkEntry(self, placeholder_text="x**2", border_color="#A5A5A5", placeholder_text_color="#A5A5A5")
        self.entradaFx.place(x=120, y=70)
        self.entradaFx.configure(width=200, height=30)

        self.labelHallar = CTkLabel(self, text="HALLAR (x):", text_color="#fff")
        self.labelHallar.place(x=50, y=120)
        self.labelHallar.configure(font=("TkDefaultFont", 12, "bold"))

        self.comboBoxHallar = CTkComboBox(self, values=["Minimización", "Maximización"])
        self.comboBoxHallar.place(x=150, y=120)
        self.comboBoxHallar.configure(width=165, height=30)

        # CONFIGURACIONES ADICIONALES
        self.labelConfigAdicionales = CTkLabel(self, text="CONFIG. ADICIONALES", text_color="#3CC0C9")
        self.labelConfigAdicionales.place(x=370, y=20)
        self.labelConfigAdicionales.configure(font=("TkDefaultFont", 24, "bold"), text_color="#FFA500")

        self.labelEliminacion = CTkLabel(self, text="ELIMINACIÓN LIMPIA", text_color="#fff")
        self.labelEliminacion.place(x=380, y=70)
        self.labelEliminacion.configure(font=("TkDefaultFont", 12, "bold"))

        self.comboBoxEliminacion = CTkComboBox(self, values=["Aplicar", "No aplicar"])
        self.comboBoxEliminacion.place(x=550, y=70)
        self.comboBoxEliminacion.configure(width=145, height=30)

        self.labelMostrarGrafica = CTkLabel(self, text="VENTANA POR GENERACIÓN", text_color="#fff")
        self.labelMostrarGrafica.place(x=380, y=120)
        self.labelMostrarGrafica.configure(font=("TkDefaultFont", 12, "bold"))

        self.comboBoxMostrarGrafica = CTkComboBox(self, values=["Si", "No"])
        self.comboBoxMostrarGrafica.place(x=615, y=120)
        self.comboBoxMostrarGrafica.configure(width=75, height=30)

        # POBLACIÓN INICIAL
        self.labelPoblacionInicial = CTkLabel(self, text="POBLACIÓN INICIAL", text_color="#3CC0C9")
        self.labelPoblacionInicial.place(x=40, y=180)
        self.labelPoblacionInicial.configure(font=("TkDefaultFont", 24, "bold"), text_color="#FFA500")

        self.labelPobMinima = CTkLabel(self, text="INICIAL", text_color="#fff")
        self.labelPobMinima.place(x=50, y=230)
        self.labelPobMinima.configure(font=("TkDefaultFont", 12, "bold"))

        self.entradaPobMinima = CTkEntry(self, placeholder_text="4", border_color="#A5A5A5", placeholder_text_color="#A5A5A5")
        self.entradaPobMinima.place(x=170, y=230)
        self.entradaPobMinima.configure(width=145, height=30)

        self.labelPobMaxima = CTkLabel(self, text="MÁXIMA", text_color="#fff")
        self.labelPobMaxima.place(x=50, y=280)
        self.labelPobMaxima.configure(font=("8", 12, "bold"))

        self.entradaPobMaxima = CTkEntry(self, placeholder_text="8", border_color="#A5A5A5", placeholder_text_color="#A5A5A5")
        self.entradaPobMaxima.place(x=170, y=280)
        self.entradaPobMaxima.configure(width=145, height=30)

        # RANGOS
        self.labelRangos = CTkLabel(self, text="RANGOS", text_color="#3CC0C9")
        self.labelRangos.place(x=370, y=170)
        self.labelRangos.configure(font=("TkDefaultFont", 24, "bold"), text_color="#FFA500")

        self.labelRangoA = CTkLabel(self, text="RANGO A:", text_color="#fff")
        self.labelRangoA.place(x=380, y=220)
        self.labelRangoA.configure(font=("TkDefaultFont", 12, "bold"))

        self.entradaRangoA = CTkEntry(self, placeholder_text="3", border_color="#A5A5A5", placeholder_text_color="#A5A5A5")
        self.entradaRangoA.place(x=480, y=220)
        self.entradaRangoA.configure(width=210, height=30)

        self.labelRangoB = CTkLabel(self, text="RANGO B:", text_color="#fff")
        self.labelRangoB.place(x=380, y=270)
        self.labelRangoB.configure(font=("TkDefaultFont", 12, "bold"))

        self.entradaRangoB = CTkEntry(self, placeholder_text="5", border_color="#A5A5A5", placeholder_text_color="#A5A5A5")
        self.entradaRangoB.place(x=480, y=270)
        self.entradaRangoB.configure(width=210, height=30)

        # MUTACIÓN
        self.labelMutacion = CTkLabel(self, text="MUTACIÓN", text_color="#3CC0C9")
        self.labelMutacion.place(x=40, y=330)
        self.labelMutacion.configure(font=("TkDefaultFont", 24, "bold"), text_color="#FFA500")

        self.labelMutacionInd = CTkLabel(self, text="% MUT. IND.:", text_color="#fff")
        self.labelMutacionInd.place(x=50, y=380)
        self.labelMutacionInd.configure(font=("TkDefaultFont", 12, "bold"))

        self.entradaMutacionInd = CTkEntry(self, placeholder_text="0.25", border_color="#A5A5A5", placeholder_text_color="#A5A5A5")
        self.entradaMutacionInd.place(x=170, y=380)
        self.entradaMutacionInd.configure(width=145, height=30)

        self.labelMutacionGen = CTkLabel(self, text="%MUT. GEN.:", text_color="#fff")
        self.labelMutacionGen.place(x=50, y=430)
        self.labelMutacionGen.configure(font=("TkDefaultFont", 12, "bold"))

        self.entradaMutacionGen = CTkEntry(self, placeholder_text="0.35", border_color="#A5A5A5", placeholder_text_color="#A5A5A5")
        self.entradaMutacionGen.place(x=170, y=430)
        self.entradaMutacionGen.configure(width=145, height=30)

        # EVALUACIÓN
        self.labelEvaluacion = CTkLabel(self, text="EVALUACIÓN", text_color="#3CC0C9")
        self.labelEvaluacion.place(x=370, y=330)
        self.labelEvaluacion.configure(font=("TkDefaultFont", 24, "bold"), text_color="#FFA500")

        self.labelIteraciones = CTkLabel(self, text="ITERACIONES:", text_color="#fff")
        self.labelIteraciones.place(x=380, y=380)
        self.labelIteraciones.configure(font=("TkDefaultFont", 12, "bold"))

        self.entradaIteraciones = CTkEntry(self, placeholder_text="5", border_color="#A5A5A5", placeholder_text_color="#A5A5A5")
        self.entradaIteraciones.place(x=490, y=380)
        self.entradaIteraciones.configure(width=200, height=30)
        
        self.labelResolucion = CTkLabel(self, text="RESOLUCIÓN:", text_color="#fff")
        self.labelResolucion.place(x=380, y=430)
        self.labelResolucion.configure(font=("TkDefaultFont", 12, "bold"))

        self.entradaResolucion = CTkEntry(self, placeholder_text="0.06", border_color="#A5A5A5", placeholder_text_color="#A5A5A5")
        self.entradaResolucion.place(x=480, y=430)
        self.entradaResolucion.configure(width=210, height=30)

        botonAlgoritmo = CTkButton(self, text="CONSTRUIR", fg_color="#FFA500", text_color="#FFFFFF", hover_color="#A8E3E7")
        botonAlgoritmo.place(x=490, y=490)
        botonAlgoritmo.configure(width=200, height=30, font=("Arial", 12, "bold"))
        botonAlgoritmo.configure(command=self.algoritmo_gen)

    def algoritmo_gen(self):
        pob_min = int(self.entradaPobMinima.get())
        pob_max = int(self.entradaPobMaxima.get())
        prob_mut_ind = float(self.entradaMutacionInd.get())
        prob_mut_gen = float(self.entradaMutacionGen.get())
        res = float(self.entradaResolucion.get())
        tipoRes = self.comboBoxHallar
        rango_Ax = float(self.entradaRangoA.get())
        rango_Bx = float(self.entradaRangoB.get())
        iteraciones = int(self.entradaIteraciones.get())
        entradaFx = self.entradaFx
        comboBoxEliminacion = self.comboBoxEliminacion
        comboBoxMostrarGrafica = self.comboBoxMostrarGrafica

        algoritmo_gen(pob_min, pob_max, prob_mut_ind, prob_mut_gen, res, tipoRes, rango_Ax, rango_Bx, iteraciones, entradaFx, comboBoxEliminacion, comboBoxMostrarGrafica)
        crear_video(images_path="./images", iteraciones=iteraciones, output_path="./video/evolution_video.mp4", fps=2)

mi_ventana = MiVentana()
mi_ventana.configure(fg_color="#1E1E1E")
mi_ventana.mainloop()
