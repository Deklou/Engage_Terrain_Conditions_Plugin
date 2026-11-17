use unity::prelude::*;

mod overlap;

#[unity::class("App", "CalculatorManager")]
pub struct CalculatorManager {}

#[unity::class("App", "CalculatorCommand")]
pub struct CalculatorCommand {}

#[unity::class("App", "GameCalculatorCommand")]
pub struct GameCalculatorCommand {}

#[unity::hook("App", "UnitCalculator", "AddCommand")]
fn register_commands(manager: &mut CalculatorManager, method: OptionalMethod) {
    call_original!(manager, method);

    if overlap::register(manager) {
        println!("[terrain_conditions] OverlayActive registered");
    } else {
        println!("[terrain_conditions] OverlayActive registration skipped");
    }
}

#[skyline::main(name = "terrain_conditions")]
pub fn main() {
    skyline::install_hooks!(register_commands);
    println!("[terrain_conditions] loaded");
}
