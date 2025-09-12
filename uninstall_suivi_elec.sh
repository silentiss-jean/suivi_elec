#!/bin/bash

echo "🧼 Désinstallation de l'intégration Suivi Élec"
echo "---------------------------------------------"
echo "Souhaitez-vous effectuer une désinstallation :"
echo "1) Totale (tout supprimer)"
echo "2) Partielle (choix par type)"
read -p "Votre choix [1/2] : " choix

expert_mode=""
if [[ "$1" == "--unlock-yaml" ]]; then
    expert_mode="je_suis_le_maître_du_yaml"
fi

if [ "$choix" == "1" ]; then
    echo "⚠️ Suppression complète en cours..."

    echo "🗑️ Suppression du dossier /config/custom_components/suivi_elec..."
    rm -rf /config/custom_components/suivi_elec/

    echo "📋 Les cartes Lovelace doivent être supprimées manuellement via l'interface."

    echo ""
    echo "📄 Analyse du fichier configuration.yaml..."
    grep -i suivi_elec /config/configuration.yaml

    echo ""
    read -p "Souhaitez-vous sauvegarder le fichier configuration.yaml avant modification ? [y/n] : " sauvegarde_yaml

    if [ "$sauvegarde_yaml" == "y" ]; then
        mkdir -p /config/suivi_elec/snapshots/
        cp /config/configuration.yaml /config/suivi_elec/snapshots/configuration_backup.yaml
        echo "✅ Fichier sauvegardé dans snapshots/configuration_backup.yaml"
    fi

    if [ "$expert_mode" == "je_suis_le_maître_du_yaml" ]; then
        echo ""
        echo "🧙 Mode expert activé. Modification automatique du fichier configuration.yaml."
        echo "\"Un bon YAML est comme un bon café : trop fort, ça te réveille... trop mal dosé, ça te crashe Home Assistant.\""
        echo ""
        echo "📜 Déroulement du parchemin secret..."
        sleep 1
        cat /config/suivi_elec/docs/expert_mode_notes.txt
        echo ""

        echo "Pour confirmer la suppression automatique des blocs liés à suivi_elec,"
        echo "tapez exactement : OUI, JE CONFIRME"
        read -p "Confirmation : " confirmation

        if [ "$confirmation" == "OUI, JE CONFIRME" ]; then
            echo "🧼 Suppression des blocs liés à suivi_elec dans configuration.yaml..."
            sed -i '/suivi_elec/,+5d' /config/configuration.yaml
            echo "✅ Modification effectuée."
        else
            echo "❌ Confirmation invalide. Aucune modification n’a été faite."
        fi
    else
        echo "ℹ️ Mode expert non activé. Aucune modification automatique du fichier configuration.yaml."
    fi

    echo "✅ Désinstallation complète terminée."

elif [ "$choix" == "2" ]; then
    echo "🔧 Désinstallation partielle — sélectionnez les éléments à supprimer :"
    read -p "Supprimer les cartes Lovelace ? [y/n] : " cartes
    read -p "Supprimer le dossier spécifique : /config/custom_components/suivi_elec ? [y/n] : " dossier

    if [ "$cartes" == "y" ]; then
        echo "📋 Les cartes Lovelace doivent être supprimées manuellement via l'interface."
    fi

    if [ "$dossier" == "y" ]; then
        echo "🗑️ Suppression du dossier /config/custom_components/suivi_elec..."
        rm -rf /config/custom_components/suivi_elec/
    fi

    echo "✅ Désinstallation partielle terminée."
else
    echo "❌ Choix invalide. Abandon."
fi
