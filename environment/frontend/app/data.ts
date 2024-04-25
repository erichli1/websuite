export const NAME_COUNTRY_ORDERDATE_ROWS = [
  {
    name: "John Doe",
    country: "USA",
    orderDate: "2024-01-02",
    id: "1",
    logLabel: "John Doe",
  },
  {
    name: "Jane Smith",
    country: "USA",
    orderDate: "2024-01-11",
    id: "2",
    logLabel: "Jane Smith",
  },
  {
    name: "Alice Johnson",
    country: "USA",
    orderDate: "2024-01-04",
    id: "3",
    logLabel: "Alice Johnson",
  },
  {
    name: "Bob Brown",
    country: "USA",
    orderDate: "2024-01-06",
    id: "4",
    logLabel: "Bob Brown",
  },
  {
    name: "Mary Davis",
    country: "Canada",
    orderDate: "2024-01-06",
    id: "5",
    logLabel: "Mary Davis",
  },
  {
    name: "Tom Wilson",
    country: "Canada",
    orderDate: "2024-01-05",
    id: "6",
    logLabel: "Tom Wilson",
  },
  {
    name: "Sara Moore",
    country: "Canada",
    orderDate: "2024-01-10",
    id: "7",
    logLabel: "Sara Moore",
  },
  {
    name: "James Taylor",
    country: "Mexico",
    orderDate: "2024-01-11",
    id: "8",
    logLabel: "James Taylor",
  },
  {
    name: "Patricia White",
    country: "Mexico",
    orderDate: "2024-01-01",
    id: "9",
    logLabel: "Patricia White",
  },
  {
    name: "Michael Harris",
    country: "Mexico",
    orderDate: "2024-01-08",
    id: "10",
    logLabel: "Michael Harris",
  },
];

export const PLAYGROUND_PRODUCTS: Array<{
  id: string;
  name: string;
  keywords: Array<string>;
  description: string;
  basePrice: number;
  customizations: {
    [key: string]: Array<{
      name: string;
      price: number;
      default?: boolean;
    }>;
  };
}> = [
  {
    id: "1",
    name: "2023 MacBook Pro - M3 chip, 14-inch",
    keywords: ["Apple", "MacBook Pro", "laptop", "computer"],
    description:
      "The 2023 MacBook Pro with a 14-inch display and an M3 chip represents a significant advancement in Apple's laptop range. The M3 chip, built on cutting-edge processing technology, delivers enhanced performance and efficiency, making it ideal for both professional and personal use. This model features a brighter and more color-accurate Liquid Retina display, which is perfect for creative professionals who require precision in their visual work. Additionally, the MacBook Pro offers improved battery life, a high-quality camera for video conferencing, and a robust thermal architecture to handle intensive tasks without overheating. The design remains sleek and portable, continuing Apple's commitment to stylish and durable products. ",
    basePrice: 1599,
    customizations: {
      memory: [
        {
          name: "8GB",
          price: 0,
          default: true,
        },
        {
          name: "16GB",
          price: 200,
        },
        {
          name: "24GB",
          price: 400,
        },
      ],
      storage: [
        {
          name: "512GB",
          price: 0,
          default: true,
        },
        {
          name: "1TB",
          price: 200,
        },
        {
          name: "2TB",
          price: 600,
        },
      ],
    },
  },
  {
    id: "2",
    name: "2023 MacBook Pro - M3 Pro chip, 14-inch",
    keywords: ["Apple", "MacBook Pro", "laptop", "computer"],
    description:
      "The 2023 MacBook Pro with the M3 Pro chip and a 14-inch display is a powerful addition to Apple's lineup, designed for professionals who need high performance and portability. This model features the new M3 Pro chip, which offers significant improvements in processing speed and graphics performance compared to its predecessors. The 14-inch Retina display provides stunning visual clarity and color accuracy, making it ideal for creative work such as video editing, graphic design, and software development. The MacBook Pro also includes enhanced connectivity options, improved battery life, and a sleek, durable design. With macOS, it offers seamless integration with Apple's ecosystem, making it a top choice for productivity and multimedia tasks.",
    basePrice: 1999,
    customizations: {
      memory: [
        {
          name: "18GB",
          price: 0,
          default: true,
        },
        {
          name: "36GB",
          price: 400,
        },
      ],
      storage: [
        {
          name: "512GB",
          price: 0,
          default: true,
        },
        {
          name: "1TB",
          price: 200,
        },
        {
          name: "2TB",
          price: 600,
        },
      ],
    },
  },
  {
    id: "3",
    name: "2024 PixelMaster Flex - QuantumCore, 15-inch",
    keywords: ["PixelMaster", "Flex", "laptop", "computer"],
    description:
      "The 2024 PixelMaster Flex boasts a 15-inch screen powered by the revolutionary QuantumCore processor. It’s designed for users who demand the best in technology and versatility. This model features a flexible hinge that allows it to transform into a tablet, enhancing its usability for design and presentations. The QuantumCore processor offers exceptional speed and multitasking capabilities, ideal for software developers and multimedia creators. Moreover, the PixelMaster Flex has a durable, lightweight design with an enhanced battery life, perfect for on-the-go professionals.",
    basePrice: 1450,
    customizations: {
      memory: [
        {
          name: "16GB",
          price: 0,
          default: true,
        },
        {
          name: "32GB",
          price: 300,
        },
      ],
      storage: [
        {
          name: "1TB",
          price: 0,
          default: true,
        },
        {
          name: "2TB",
          price: 350,
        },
      ],
    },
  },
  {
    id: "4",
    name: "2024 ZenithEdge Z3 - HyperX Processor, 13-inch",
    keywords: ["ZenithEdge", "Z3", "laptop", "computer"],
    description:
      "Introducing the ZenithEdge Z3 with a 13-inch display and the HyperX processor, tailored for ultra-efficient performance. The HyperX processor is designed to provide a balance between power consumption and performance, making it ideal for extended mobile use without sacrificing speed. This compact model is equipped with a high-resolution display and a robust, light frame, making it a favorite for travelers and business professionals alike. The Z3 offers quick charging capabilities and superior connectivity options, ensuring productivity is never hindered.",
    basePrice: 1200,
    customizations: {
      memory: [
        {
          name: "8GB",
          price: 0,
          default: true,
        },
        {
          name: "16GB",
          price: 200,
        },
      ],
      storage: [
        {
          name: "256GB",
          price: 0,
          default: true,
        },
        {
          name: "512GB",
          price: 150,
        },
      ],
    },
  },
  {
    id: "5",
    name: "2024 NovaPro Orbit - Starlight Processor, 16-inch",
    keywords: ["NovaPro", "Orbit", "laptop", "computer"],
    description:
      "The 2024 NovaPro Orbit features a 16-inch display equipped with the Starlight Processor, targeting gamers and graphic designers. It delivers unparalleled graphics performance and a high-refresh-rate screen for smooth visuals. This model also includes customizable RGB lighting and a cutting-edge cooling system to handle intense gaming sessions and heavy graphical tasks. The Orbit’s robust build and sleek design make it an appealing choice for those who prioritize both aesthetics and functionality in their computing devices.",
    basePrice: 2100,
    customizations: {
      memory: [
        {
          name: "32GB",
          price: 0,
          default: true,
        },
        {
          name: "64GB",
          price: 500,
        },
      ],
      storage: [
        {
          name: "1TB",
          price: 0,
          default: true,
        },
        {
          name: "2TB",
          price: 400,
        },
      ],
    },
  },
  {
    id: "6",
    name: "2024 EchoStream Vortex - DualTech Engine, 14-inch",
    keywords: ["EchoStream", "Vortex", "laptop", "computer"],
    description:
      "The 2024 EchoStream Vortex, with a 14-inch screen and DualTech Engine, is optimized for creators and tech enthusiasts. The DualTech Engine provides high efficiency and rapid processing speeds, suitable for video editing, 3D modeling, and advanced computing tasks. This laptop features a high-fidelity sound system and an advanced connectivity suite, making it perfect for multimedia consumption and professional use. Its robust, minimalist design and enhanced battery life also ensure it stands out in the market for stylish yet powerful laptops.",
    basePrice: 1800,
    customizations: {
      memory: [
        {
          name: "16GB",
          price: 0,
          default: true,
        },
        {
          name: "32GB",
          price: 300,
        },
      ],
      storage: [
        {
          name: "512GB",
          price: 0,
          default: true,
        },
        {
          name: "1TB",
          price: 250,
        },
      ],
    },
  },
  {
    id: "7",
    name: "2024 TerraTech Prism - CoreX9, 17-inch",
    keywords: ["TerraTech", "Prism", "laptop", "computer"],
    description:
      "The 2024 TerraTech Prism with a 17-inch display and the CoreX9 chipset redefines high-performance computing. Ideal for data scientists and AI researchers, this model provides massive computational power to handle complex algorithms and large data sets. The Prism's large, ultra-clear display enhances visibility and productivity, while its robust security features ensure data integrity. With a premium, lightweight design and all-day battery life, the Prism is a powerhouse designed for the highest demands of modern computing.",
    basePrice: 2300,
    customizations: {
      memory: [
        {
          name: "64GB",
          price: 0,
          default: true,
        },
        {
          name: "128GB",
          price: 700,
        },
      ],
      storage: [
        {
          name: "2TB",
          price: 0,
          default: true,
        },
        {
          name: "4TB",
          price: 800,
        },
      ],
    },
  },
];
