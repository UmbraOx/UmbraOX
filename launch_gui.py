from core.ui.umbra_control_center import UmbraControlCenter

# You will wire real spine here from run_umbra
def launch(spine):
    ui = UmbraControlCenter(spine=spine)
    ui.run()