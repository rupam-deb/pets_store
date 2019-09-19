{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "name": "Untitled8.ipynb",
      "provenance": [],
      "collapsed_sections": [],
      "include_colab_link": true
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
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
        "<a href=\"https://colab.research.google.com/github/rupam-deb/pets_store/blob/synengcotest/anomalydetection.py\" target=\"_parent\"><img src=\"https://colab.research.google.com/assets/colab-badge.svg\" alt=\"Open In Colab\"/></a>"
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "57D8GVR2dHv3",
        "colab_type": "code",
        "outputId": "0286e7e1-2f0e-4714-ff14-22170eae604b",
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 72
        }
      },
      "source": [
        "'''\n",
        "@Description: Additional Task number three: Additional Task - Anomaly detection\n",
        "@Written By: Rupam Deb\n",
        "@Platform: Python GoogleCoLab\n",
        "'''\n",
        "\n",
        "# IMPORT REQUIRED LIBRARY\n",
        "import os\n",
        "import pandas as pd\n",
        "import numpy as np\n",
        "import datetime\n",
        "from datetime import timedelta\n",
        "import csv\n",
        "from matplotlib import pyplot as plt\n",
        "\n",
        "# MOVING AVERAGE\n",
        "def moving_average(x, w):\n",
        "    ma = np.convolve(x, np.ones(w), mode='valid') / w\n",
        "    return np.concatenate([np.zeros(w-1)*np.nan, ma])\n",
        "  \n",
        "# ROLLING STANDARD DEVIATION\n",
        "def moving_standard_deviation(a, window):\n",
        "    # Rolling standard deviation.\n",
        "    shape = a.shape[:-1] + (a.shape[-1] - window + 1, window)\n",
        "    strides = a.strides + (a.strides[-1],)\n",
        "    sd = np.lib.stride_tricks.as_strided(a, shape=shape, strides=strides)\n",
        "    # Library: numpy.std(a, axis=None, dtype=None, out=None, ddof=0, keepdims=<no value>)\n",
        "    # Source: https://docs.scipy.org/doc/numpy/reference/generated/numpy.std.html\n",
        "    print(sd[5])\n",
        "    sd_data = np.std(sd, axis = 1)\n",
        "    # Behaviour similarly to the `moving_average` function.\n",
        "    return np.concatenate([np.zeros(window-1)*np.nan, sd_data])\n",
        "  \n",
        "# MAIN ANOMALY DETECTION FUNCTION\n",
        "def detect_anomalies(time, signal1, signal2, base_window, test_window):\n",
        "  # check that inputs have the same shape\n",
        "  if (time.shape == signal1.shape == signal2.shape):\n",
        "    # check that input is long enough for the base window stats\n",
        "    if (len(time) > base_window):\n",
        "      # calculate a simple feature from the 2 signals\n",
        "      feature = signal1 - signal2\n",
        "      # calculate a mean shift score from the data\n",
        "      mean_shift = np.zeros(time.shape)\n",
        "      # CALL MOVING AVERAGE for BASE sliding\n",
        "      base_mean = moving_average(feature, base_window)\n",
        "      # CALL MOVING AVERAGE FOR TESTING sliding\n",
        "      test_mean = moving_average(feature, test_window)\n",
        "      #CALL ROLLING STANDARD DEVIATION\n",
        "      base_std = moving_standard_deviation(feature, base_window)\n",
        "    \n",
        "      # CATCH ERuntimeWarning: divide by zero encountered in true_divide\n",
        "      nan = float('nan')\n",
        "      for j in range(1464):\n",
        "        if(base_std[j] == 0):\n",
        "          base_std[j] = nan\n",
        "        \n",
        "      mean_shift = (test_mean - base_mean)/base_std\n",
        "      \n",
        "      # PREPARE WRITER\n",
        "      corpus_write = os.path.join(\"/content/gdrive/My Drive/data\", \"weather_BOM_OTHER DATA.csv\")\n",
        "      myData = mean_shift\n",
        "      myFile = open(corpus_write, 'a')\n",
        "      with myFile:\n",
        "        writer = csv.writer(myFile)\n",
        "        writer.writerow(myData)\n",
        "      # detect anomalies based on the mean shift score\n",
        "      anomalies = []\n",
        "      \n",
        "      # Generate a list of times where the mean_shift is greater than or less than 1.0\n",
        "      list_of_time = []\n",
        "      for j in range(1464):\n",
        "        if((mean_shift[j] > 1) or (mean_shift[j] < 1)):\n",
        "          list_of_time.append(time[j])\n",
        "      #print(list_of_time)    \n",
        "      return {\n",
        "        'feature': feature,\n",
        "        'mean_shift': mean_shift,\n",
        "        'anomalies': np.array(anomalies),\n",
        "      }\n",
        "      \n",
        "    else:\n",
        "      print('Argument arrays are not long enough')\n",
        "      \n",
        "  else:\n",
        "    print('The shapes of three fields (date, BOM data, and Weather Station data) are not same')\n",
        "\n",
        "# MOUNT DRIVE\n",
        "from google.colab import drive\n",
        "drive.mount('/content/gdrive')\n",
        "corpus = os.path.join(\"/content/gdrive/My Drive/data\", \"weather_BOM.csv\")\n",
        "# READ FILE\n",
        "df = pd.read_csv(corpus)\n",
        "# CONVERT INPUTS to NUMPY ARRAY\n",
        "time = np.array(df['date'])\n",
        "signal1 = np.array(df['BOM Data'])\n",
        "signal2 = np.array(df['Weather Station Data'])   \n",
        "Data = detect_anomalies(time, signal1, signal2, base_window=10, test_window=3)\n",
        "\n"
      ],
      "execution_count": 20,
      "outputs": [
        {
          "output_type": "stream",
          "text": [
            "Drive already mounted at /content/gdrive; to attempt to forcibly remount, call drive.mount(\"/content/gdrive\", force_remount=True).\n",
            "[  14.36    14.36    -6.035 -210.245 -291.265 -339.06  -349.24  -312.94\n",
            " -170.855 -115.775]\n"
          ],
          "name": "stdout"
        }
      ]
    }
  ]
}