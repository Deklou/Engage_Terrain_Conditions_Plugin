use unity::prelude::*;

#[allow(dead_code)]
mod overlap;

#[unity::class("App", "CalculatorManager")]
pub struct CalculatorManager {}

#[unity::class("App", "CalculatorCommand")]
pub struct CalculatorCommand {}

#[unity::class("App", "GameCalculatorCommand")]
pub struct GameCalculatorCommand {}

// Engage 2.0.0: App.UnitCalculator.AddCommand
// Use the verified offset instead of resolving IL2CPP metadata during NRO loading.
#[skyline::hook(offset = 0x01F726A0)]
fn register_commands(manager: &mut CalculatorManager, method: OptionalMethod) {
    println!("[terrain_conditions] AddCommand enter");
    call_original!(manager, method);
    println!("[terrain_conditions] AddCommand returned");
    // OverlayActive registration stays off until this hook is validated in game.
}

#[skyline::main(name = "terrain_conditions")]
pub fn main() {
    println!("[terrain_conditions] installing AddCommand hook");
    skyline::install_hooks!(register_commands);
    println!("[terrain_conditions] loaded");
}
