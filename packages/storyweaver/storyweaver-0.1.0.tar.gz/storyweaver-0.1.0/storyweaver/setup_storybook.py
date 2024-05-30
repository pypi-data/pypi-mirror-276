import os
import sys
import argparse

def create_storybook_config(addons):
    # Configure Storybook (if necessary)
    print("Configuring Storybook...")
    
    main_js_content = f"""
module.exports = {{
  stories: ['../src/**/*.stories.@(js|jsx|ts|tsx|mdx)'],
  addons: [
    {', '.join(f"'{addon}'" for addon in addons)}
  ],
}};
"""
    preview_js_content = """
export const parameters = {
  actions: { argTypesRegex: "^on[A-Z].*" },
  controls: {
    matchers: {
      color: /(background|color)$/i,
      date: /Date$/,
    },
  },
};
"""
    os.makedirs('.storybook', exist_ok=True)
    with open('.storybook/main.js', 'w') as f:
        f.write(main_js_content)
    with open('.storybook/preview.js', 'w') as f:
        f.write(preview_js_content)

def generate_stories(root_dir):
    # Generate stories for each component
    print(f"Generating stories for components in {root_dir}...")

    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if (file.endswith('.js') or file.endswith('.jsx') or file.endswith('.ts') or file.endswith('.tsx')) and not file.endswith('.stories.js') and not file.endswith('.stories.ts'):
                component_name = file.split('.')[0]
                component_path = os.path.join(root, file)
                story_path = os.path.join(root, f"{component_name}.stories.{file.split('.')[-1]}")

                if not os.path.exists(story_path):
                    with open(story_path, 'w') as f:
                        f.write(f"""import React from 'react';
import {component_name} from './{file}';

export default {{
  title: '{component_name}',
  component: {component_name},
}};

const Template = (args) => <{component_name} {{...args}} />;

export const Primary = Template.bind({});
Primary.args = {{
  // Add default props here
}};
""")
                    print(f"Generated story for {component_name} at {story_path}")
                else:
                    print(f"Story already exists for {component_name}, skipping...")

def main():
    parser = argparse.ArgumentParser(description='Setup Storybook and generate stories for React components.')
    parser.add_argument('components_directory', type=str, help='The directory containing the React components.')
    parser.add_argument('--addons', nargs='*', default=['@storybook/addon-links', '@storybook/addon-essentials'], help='List of Storybook addons to include.')

    args = parser.parse_args()

    create_storybook_config(args.addons)
    generate_stories(args.components_directory)
    print("Storybook setup completed successfully.")

if __name__ == '__main__':
    main()
