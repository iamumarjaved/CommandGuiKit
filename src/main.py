from cement import App, Controller, ex
from gooey import Gooey, GooeyParser
import icli

# Gooey-specific argument handling in the GUI
@Gooey(program_name="Advanced CLI-GUI Application",
       default_size=(600, 800),
       navigation='SIDEBAR',
       sidebar_title="Command Categories",
       body_bg_color='#f2f2f2',
       header_bg_color='#4B77BE',
       footer_bg_color='#4B77BE',
       header_show_title=True,
       header_show_subtitle=True,
       richtext_controls=False,
       clear_before_run=True)
def main_gui():
    # Create GooeyParser for GUI argument handling
    parser = GooeyParser(description="CLI-GUI App")
    
    # GUI Inputs
    parser.add_argument('--command', help='Choose a command', choices=['dynamic-cli', 'enhanced-cli', 'interactive'], required=True)
    parser.add_argument('--file', help='Path to input file', widget='FileChooser', gooey_options={'visible': True})
    parser.add_argument('--save', help='Save output to file', action='store_true')
    parser.add_argument('--format', help='Output format', choices=['json', 'xml', 'csv'], default='json')
    parser.add_argument('--name', help='Your name', type=str, default='User')
    parser.add_argument('--greet', help='Custom greeting', action='store', type=str, default='Hello')
    parser.add_argument('--repeat', help='Number of times to repeat the greeting', type=int, default=1)

    args = parser.parse_args()

    # Build the command that will be passed to Cement
    command = args.command  # Fetch the user's choice for the command
    
    # Create the argument list for Cement
    cement_args = [command]
    
    # For dynamic-cli, automatically use the 'greet' subcommand
    if command == 'dynamic-cli':
        cement_args.append('greet')
    
    # Append additional arguments for the command
    if args.file and command == 'enhanced-cli':
        cement_args.extend(['--file', args.file])
    if args.save and command == 'enhanced-cli':
        cement_args.append('--save')
    if command == 'enhanced-cli':
        cement_args.extend(['--format', args.format])

    # Add arguments specific to dynamic-cli commands
    if command == 'dynamic-cli':
        cement_args.extend(['--name', args.name])
        cement_args.extend(['--greet', args.greet])
        cement_args.extend(['--repeat', str(args.repeat)])

    # Pass arguments to Cement app
    with CommandGuiKit(argv=cement_args) as app:
        app.run()

class EnhancedCLIController(Controller):
    class Meta:
        label = 'enhanced_cli'
        stacked_on = 'base'
        stacked_type = 'nested'
        arguments = [
            (['--file'], {'help': 'Path to input file'}),
            (['--save'], {'help': 'Save output to file', 'action': 'store_true'}),
            (['--format'], {'help': 'Output format', 'choices': ['json', 'xml', 'csv'], 'default': 'json'})
        ]

    @ex(help='Process file and save output')
    def process_file(self):
        file = self.app.pargs.file
        file_format = self.app.pargs.format
        print(f"Processing file: {file}, Format: {file_format}")

class DynamicCLIController(Controller):
    class Meta:
        label = 'dynamic_cli'
        stacked_on = 'base'
        stacked_type = 'nested'
        arguments = [
            (['--name'], {'help': 'Your name', 'type': str, 'default': 'User'}),
            (['--greet'], {'help': 'Custom greeting', 'action': 'store', 'type': str, 'default': 'Hello'}),
            (['--repeat'], {'help': 'Number of times to repeat the greeting', 'type': int, 'default': 1})
        ]

    @ex(help='Greet dynamically')
    def greet(self):
        name = self.app.pargs.name
        greeting = self.app.pargs.greet
        repeat = self.app.pargs.repeat
        for _ in range(repeat):
            print(f"{greeting}, {name}!")

class InteractiveController(Controller):
    class Meta:
        label = 'interactive'
        stacked_on = 'base'
        stacked_type = 'nested'
        description = "Interactive commands via icli."

    def _default(self):
        icli.run_interactive()

class MyBaseController(Controller):
    class Meta:
        label = 'base'
        description = "Base controller for the application."

    def _default(self):
        print("Base controller for navigation and help.")

class CommandGuiKit(App):
    class Meta:
        label = 'CommandGuiKit'
        base_controller = 'base'
        handlers = [EnhancedCLIController, DynamicCLIController, InteractiveController, MyBaseController]

    def __init__(self, *args, **kwargs):
        # Capture GUI arguments from Gooey
        super().__init__(*args, **kwargs)

if __name__ == '__main__':
    main_gui()
