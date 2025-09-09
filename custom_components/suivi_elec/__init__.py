from .launcher import run_all

async def async_setup(hass, config):
    async def handle_generate(call):
        run_all()
        hass.components.persistent_notification.create(
            "✅ Fichiers de suivi générés avec succès.",
            title="Suivi Élec"
        )

    hass.services.async_register("suivi_elec", "generate_config", handle_generate)
    return True