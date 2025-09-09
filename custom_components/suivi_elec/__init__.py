from custom_components.suivi_elec.launcher import run_all

def setup(hass, config):
    def handle_service(call):
        run_all()
    hass.services.register("suivi_elec", "generate_suivi_elec", handle_service)
    return True
