from django.shortcuts import render

# Create your views here.

def news(request):
    titulo = "AgriTech"
    historia = '''
                
                Una huerta comunitaria es un espacio de cultivo colectivo en el que un grupo de personas se organiza para sembrar, cuidar y cosechar diferentes tipos de plantas, principalmente alimentos como hortalizas, frutas, legumbres o hierbas medicinales. Este tipo de iniciativa  también  busca promover la cooperación entre vecinos, la educación ambiental y el aprovechamiento de espacios urbanos o rurales que, de otra manera, podrían estar en desuso. 

                Además, las huertas comunitarias fomentan hábitos de vida más sostenibles, ya que contribuyen a la seguridad alimentaria, fortalecen los lazos sociales, permiten aprender técnicas de cultivo respetuosas con el medio ambiente y acercan a las personas al origen de los alimentos. En muchos casos, también funcionan como espacios de encuentro, intercambio de saberes y apoyo mutuo, generando beneficios tanto a nivel individual como colectivo.               '''

    trabajos = '''
               
                Este proyecto nació en 2021, cuando a raíz de las dificultades generadas por la pandemia y el estallido social, profesores y comunidad educativa se unieron y solicitaron soporte tecnológico para su desarrollo.                 La agricultura de precisión combina servicios de tecnologías de la información y las comunicaciones, a través de sistemas de conectividad y energía solar, mediante una aplicación que permite el acceso a internet y los equipos de monitoreo en tiempo real,
                 
                '''

    estacion = '''
                Se creó una estación que permite monitorear de manera precisa las condiciones ambientales y del suelo en una huerta, con el fin de optimizar el cuidado de los cultivos. Esta estación mide variables como la humedad, la temperatura, la velocidad y dirección del viento, la concentración de fósforo en el suelo y la intensidad de la luz solar. Gracias a esta información es posible saber en qué momento es necesario regar, prevenir el exceso de agua, anticipar riesgos de heladas o altas temperaturas, ajustar la fertilización según la disponibilidad de nutrientes y comprender cómo la radiación solar influye en el crecimiento de las plantas. De esta manera, la estación facilita una gestión más eficiente de los recursos y ademas contribuye a mejorar la productividad, reducir costos y fomentar prácticas agrícolas sostenibles dentro de la huerta comunitaria.
               '''

    return(render(request, 'news.html',  { 
                                            'width': 'w-20',
                                            'historia': historia,
                                            'trabajos': trabajos,
                                            'estacion': estacion
     }))
