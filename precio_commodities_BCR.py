{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "provenance": [],
      "collapsed_sections": [
        "IcnAkr6pjfla"
      ],
      "authorship_tag": "ABX9TyM9n5xW3EyO0VrmzGVpweG7",
      "include_colab_link": true
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    },
    "language_info": {
      "name": "python"
    }
  },
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "view-in-github",
        "colab_type": "text"
      },
      "source": [
        "<a href=\"https://colab.research.google.com/github/AlejandroYegrosSchmidt/py.data_free/blob/main/precio_commodities_BCR.ipynb\" target=\"_parent\"><img src=\"https://colab.research.google.com/assets/colab-badge.svg\" alt=\"Open In Colab\"/></a>"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "id": "mvA0WlkTKFk7"
      },
      "outputs": [],
      "source": [
        "import time\n",
        "import urllib\n",
        "import urllib.request\n",
        "from bs4 import BeautifulSoup"
      ]
    },
    {
      "cell_type": "markdown",
      "source": [
        "# Programa para extraer el precio de los commodities de la Bolsa de comercio de Rosario"
      ],
      "metadata": {
        "id": "IcnAkr6pjfla"
      }
    },
    {
      "cell_type": "code",
      "source": [
        "class datatree():\n",
        "    def __init__(self,endpoint=None):\n",
        "        self.endpoint = endpoint\n",
        "        self.url = f'https://www.bcr.com.ar/es/mercados/mercado-de-granos/cotizaciones/cotizaciones-internacionales/chicagokansas-cme-group-{self.endpoint}'\n",
        "\n",
        "    def bs4_soup(self):\n",
        "        thepage = urllib.request.urlopen(self.url)\n",
        "        soup = BeautifulSoup(thepage,\"html.parser\")\n",
        "        fecha_cierre=soup.find(class_=\"c1\",colspan=\"5\")\n",
        "        fecha_cierre = fecha_cierre.get_text()\n",
        "        return soup, fecha_cierre\n",
        "\n",
        "    def select_tabla(self):\n",
        "        #### manejo de errores###\n",
        "        # En ocasiones la pagina cambia el nombre de la tabla a ser extraída,\n",
        "        # por lo que es necesario menejar el error agregando las excepciones, es decir los nombres de las tablas\n",
        "        soup, fecha_cierre = self.bs4_soup()\n",
        "        opcion = ['sheet','sheet--12','sheet--2','sheet--3']\n",
        "        for i in opcion:\n",
        "            try:\n",
        "                tabla = soup.find(id=i, class_=\"table\")\n",
        "                td = tabla.find_all(\"td\")\n",
        "                tr = tabla.find_all(\"tr\")\n",
        "            except:\n",
        "                pass\n",
        "        return td, tr,fecha_cierre\n",
        "\n",
        "    def commodities_prices(self):\n",
        "        td, tr,fecha_cierre = self.select_tabla()\n",
        "        cantidad_tr_fila = len(tr)- 5  # cantidad de tr/filas en la tabla, se resta 3 tr que corresponden al encabezado de la tablas y 2 tr que corresponden al pie de la tabla\n",
        "        cantidad_td =len(td)\n",
        "        campofecha_X = 11  # La fecha inicia en el td 11\n",
        "        campofecha_Y = len(td) - campofecha_X - 1\n",
        "\n",
        "        ## ubicamos las columas de cada precio de los commodities\n",
        "        Trigo_Chicago_1_X= campofecha_X+1\n",
        "        Trigo_Chicago_1_Y= campofecha_Y-1\n",
        "\n",
        "        Trigo_Chicago_2_X= campofecha_X+3\n",
        "        Trigo_Chicago_2_Y= campofecha_Y-3\n",
        "\n",
        "        Maiz_Chicago_3_X= campofecha_X+5\n",
        "        Maiz_Chicago_3_Y= campofecha_Y-5\n",
        "\n",
        "        Soja_Chicago_4_X= campofecha_X+7\n",
        "        Soja_Chicago_4_Y= campofecha_Y-7\n",
        "\n",
        "        AceiteSoja_Chicago_5_X= campofecha_X+9\n",
        "        AceiteSoja_Chicago_5_Y= campofecha_Y-9\n",
        "\n",
        "        HarinaSoja_Chicago_6_X= campofecha_X+11\n",
        "        HarinaSoja_Chicago_6_Y= campofecha_Y-11\n",
        "\n",
        "        contador = 0\n",
        "        datos = []\n",
        "        while contador != cantidad_tr_fila:\n",
        "            ## el primer bucle for extrae las fechas de los contratos\n",
        "            for i in td[campofecha_X:-campofecha_Y]:\n",
        "                fecha_contrato_futuro = i.text\n",
        "                fecha_contrato_futuro = (str.replace(fecha_contrato_futuro, \"Dic\", \"01/12\"))\n",
        "                fecha_contrato_futuro = (str.replace(fecha_contrato_futuro, \"Nov\", \"01/11\"))\n",
        "                fecha_contrato_futuro = (str.replace(fecha_contrato_futuro, \"Oct\", \"01/10\"))\n",
        "                fecha_contrato_futuro = (str.replace(fecha_contrato_futuro, \"Sep\", \"01/09\"))\n",
        "                fecha_contrato_futuro = (str.replace(fecha_contrato_futuro, \"Ago\", \"01/08\"))\n",
        "                fecha_contrato_futuro = (str.replace(fecha_contrato_futuro, \"Jul\", \"01/07\"))\n",
        "                fecha_contrato_futuro = (str.replace(fecha_contrato_futuro, \"Jun\", \"01/06\"))\n",
        "                fecha_contrato_futuro = (str.replace(fecha_contrato_futuro, \"May\", \"01/05\"))\n",
        "                fecha_contrato_futuro = (str.replace(fecha_contrato_futuro, \"Abr\", \"01/04\"))\n",
        "                fecha_contrato_futuro = (str.replace(fecha_contrato_futuro, \"Mar\", \"01/03\"))\n",
        "                fecha_contrato_futuro = (str.replace(fecha_contrato_futuro, \"Feb\", \"01/02\"))\n",
        "                fecha_contrato_futuro = (str.replace(fecha_contrato_futuro, \"Ene\", \"01/01\"))\n",
        "                fecha_contrato_futuro = (str.replace(fecha_contrato_futuro, \"-\", \"/\"))\n",
        "                fecha_contrato_futuro = fecha_contrato_futuro\n",
        "                campofecha_X=campofecha_X + 13\n",
        "                campofecha_Y = campofecha_Y -13\n",
        "\n",
        "            ## a partir de estos bucles se extraen los precios de los los contratos\n",
        "            for i in td[Trigo_Chicago_1_X:-Trigo_Chicago_1_Y]:\n",
        "                TrigoChicago1 = i.text\n",
        "                if TrigoChicago1 == \"\":\n",
        "                    TrigoChicago1 = \"0,0\"\n",
        "                TrigoChicago1 = float(TrigoChicago1.replace(\",\",\".\"))\n",
        "                Trigo_Chicago_1_X=Trigo_Chicago_1_X+13\n",
        "                Trigo_Chicago_1_Y=Trigo_Chicago_1_Y-13\n",
        "\n",
        "            for i in td[Trigo_Chicago_2_X:-Trigo_Chicago_2_Y]:\n",
        "                TrigoChicago2 = i.text\n",
        "                if TrigoChicago2 == \"\":\n",
        "                    TrigoChicago2 = \"0,0\"\n",
        "                TrigoChicago2 = float(TrigoChicago2.replace(\",\", \".\"))\n",
        "                Trigo_Chicago_2_X = Trigo_Chicago_2_X + 13\n",
        "                Trigo_Chicago_2_Y = Trigo_Chicago_2_Y - 13\n",
        "\n",
        "            for i in td[Maiz_Chicago_3_X:-Maiz_Chicago_3_Y]:\n",
        "                MaizChicago3 = i.text\n",
        "                if MaizChicago3 == \"\":\n",
        "                    MaizChicago3 = \"0,0\"\n",
        "                MaizChicago3 = float(MaizChicago3.replace(\",\",\".\"))\n",
        "                Maiz_Chicago_3_X = Maiz_Chicago_3_X + 13\n",
        "                Maiz_Chicago_3_Y = Maiz_Chicago_3_Y - 13\n",
        "\n",
        "            for i in td[Soja_Chicago_4_X:-Soja_Chicago_4_Y]:\n",
        "                SojaChicago4 = i.text\n",
        "                if SojaChicago4 == \"\":\n",
        "                    SojaChicago4 = \"0,0\"\n",
        "                SojaChicago4 = float(SojaChicago4.replace(\",\", \".\"))\n",
        "                Soja_Chicago_4_X = Soja_Chicago_4_X + 13\n",
        "                Soja_Chicago_4_Y = Soja_Chicago_4_Y - 13\n",
        "\n",
        "            for i in td[AceiteSoja_Chicago_5_X:-AceiteSoja_Chicago_5_Y]:\n",
        "                AceiteSojaChicago5 = i.text\n",
        "                if AceiteSojaChicago5 == \"\":\n",
        "                    AceiteSojaChicago5 = \"0,0\"\n",
        "                AceiteSojaChicago5 = float(AceiteSojaChicago5.replace(\",\", \".\"))\n",
        "                AceiteSoja_Chicago_5_X = AceiteSoja_Chicago_5_X + 13\n",
        "                AceiteSoja_Chicago_5_Y = AceiteSoja_Chicago_5_Y - 13\n",
        "\n",
        "            for i in td[HarinaSoja_Chicago_6_X:-HarinaSoja_Chicago_6_Y]:\n",
        "                HarinaSojaChicago6 = i.text\n",
        "                if HarinaSojaChicago6  == \"\":\n",
        "                    HarinaSojaChicago6  = \"0,0\"\n",
        "                HarinaSojaChicago6  = float(HarinaSojaChicago6 .replace(\",\", \".\"))\n",
        "                HarinaSoja_Chicago_6_X = HarinaSoja_Chicago_6_X + 13\n",
        "                HarinaSoja_Chicago_6_Y = HarinaSoja_Chicago_6_Y - 13\n",
        "\n",
        "            datos.append([fecha_contrato_futuro, TrigoChicago1, TrigoChicago2, MaizChicago3, SojaChicago4, AceiteSojaChicago5, HarinaSojaChicago6, fecha_cierre,self.endpoint])\n",
        "            #print(fecha_contrato_futuro, \"-\", TrigoChicago1, \"-\", TrigoChicago2, \"-\", MaizChicago3, \"-\", SojaChicago4,\"-\",AceiteSojaChicago5,\"-\",HarinaSojaChicago6,\"-\", fecha_cierre, 'Realizado', contador)\n",
        "            contador += 1\n",
        "        return datos\n"
      ],
      "metadata": {
        "id": "SsYIoE6IZTJn"
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "tree = datatree(endpoint= \"2955\")\n",
        "#print(tree.commodities_prices())\n",
        "datos = tree.commodities_prices()"
      ],
      "metadata": {
        "id": "dhbzHVATZoPp"
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "markdown",
      "source": [
        "# Extrar datos bajo demanda"
      ],
      "metadata": {
        "id": "iySMsM4bkX2z"
      }
    },
    {
      "cell_type": "code",
      "source": [
        "import pandas as pd\n",
        "# El endpoint son los numero finales que aparecen al final de la url\n",
        "# 'https://www.bcr.com.ar/es/mercados/mercado-de-granos/cotizaciones/cotizaciones-internacionales/chicagokansas-cme-group-2953'\n",
        "\n",
        "\n",
        "class BCR_commodities_prices:\n",
        "    def __init__(self):\n",
        "        \"\"\"\n",
        "        Inicializa la clase con el rango de endpoints, pidiéndolos al usuario.\n",
        "        \"\"\"\n",
        "        self.datafrom = int(input(\"Ingrese el endpoint inicial: \"))\n",
        "        self.datato = int(input(\"Ingrese el endpoint final: \"))\n",
        "\n",
        "    def tabla_datos(self):\n",
        "        \"\"\"\n",
        "        Obtiene los datos de commodities para el rango de endpoints y los organiza en un DataFrame.\n",
        "        \"\"\"\n",
        "        bd = {\n",
        "            \"fecha_contrato_futuro\": [],\n",
        "            \"trigo_chicago_1\": [],\n",
        "            \"trigo_chicago_2\": [],\n",
        "            \"maiz_chicago_3\": [],\n",
        "            \"soja_chicago_4\": [],\n",
        "            \"aceite_soja_chicago_5\": [],\n",
        "            \"harina_soja_chicago_6\": [],\n",
        "            \"fecha_cierre\": [],\n",
        "            \"endpoint\": []\n",
        "        }\n",
        "\n",
        "        for i in range(self.datafrom, self.datato):\n",
        "            try:\n",
        "                datos = datatree(endpoint=i).commodities_prices()\n",
        "                # Validar que los datos tengan la longitud esperada\n",
        "                for _ in datos:\n",
        "                    if datos and len(datos[0]) >= 9:\n",
        "                        bd[\"fecha_contrato_futuro\"].append(datos[0][0])\n",
        "                        bd[\"trigo_chicago_1\"].append(datos[0][1])\n",
        "                        bd[\"trigo_chicago_2\"].append(datos[0][2])\n",
        "                        bd[\"maiz_chicago_3\"].append(datos[0][3])\n",
        "                        bd[\"soja_chicago_4\"].append(datos[0][4])\n",
        "                        bd[\"aceite_soja_chicago_5\"].append(datos[0][5])\n",
        "                        bd[\"harina_soja_chicago_6\"].append(datos[0][6])\n",
        "                        bd[\"fecha_cierre\"].append(datos[0][7])\n",
        "                        bd[\"endpoint\"].append(datos[0][8])\n",
        "                    else:\n",
        "                        print(f\"Datos incompletos o vacíos para el endpoint {i}\")\n",
        "            except Exception as e:\n",
        "                print(f\"Error procesando el endpoint {i}: {e}\")\n",
        "\n",
        "        df = pd.DataFrame(bd)\n",
        "        return df"
      ],
      "metadata": {
        "id": "RHK89KxRkVvK"
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "#BCR_commodities_prices().tabla_datos()"
      ],
      "metadata": {
        "id": "3LU4Pxh7-aPm"
      },
      "execution_count": null,
      "outputs": []
    }
  ]
}