declare const require: any;
export class Demo {
  name: string;
  constructor(name: string) {
    this.name = name;
  }
  greet(): string {
    return `Hello, ${this.name}! This is a TypeScript demo.`;
  }
}

function main(): void {
  const name = process.argv[2] ?? "World";
  const d = new Demo(name);
  console.log(d.greet());
}

if (typeof require !== "undefined" && require.main === module) {
  main();
}
