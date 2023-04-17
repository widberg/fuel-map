#include <CImg.h>
#include <CLI/CLI.hpp>
#include <atomic>
#include <algorithm>
#include <cstdint>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <string>
#include <vector>

using namespace cimg_library;

struct LookupDescription {
    std::uint32_t a : 12;
    std::uint32_t b : 20;
};

void lookup_float(std::uint32_t x, std::uint32_t y, std::uint32_t num,
                  std::uint32_t limit, std::uint32_t *float_data,
                  LookupDescription *lookup, float result[4][4]) {
  std::uint32_t *float_data_negative_ptr = float_data - limit * 2;

  LookupDescription *lookup_1 = &lookup[(x / 4) + num * (y / 4)];

  std::uint32_t four_times_sub_y = 4 * (y % 4);
  for (std::uint32_t i = 0; i < 4; ++i) {
    LookupDescription lookup_desc = lookup_1[0];
    LookupDescription lookup_desc_1 = lookup_1[1];
    switch (x % 4) {
    case 0: {
      if (lookup_desc.b < limit) {
        std::uint8_t *v17 = (std::uint8_t *)&float_data[2 * lookup_desc.b] + (four_times_sub_y >> 1);
        result[i][0] = lookup_desc.a + (v17[0] >> 4);
        result[i][1] = lookup_desc.a + (v17[0] & 0xF);
        result[i][2] = lookup_desc.a + (v17[1] >> 4);
        result[i][3] = lookup_desc.a + (v17[1] & 0xFu);
      } else {
        std::uint8_t *v14 = (std::uint8_t *)float_data_negative_ptr + four_times_sub_y + 16 * lookup_desc.b;
        result[i][0] = lookup_desc.a + v14[0];
        result[i][1] = lookup_desc.a + v14[1];
        result[i][2] = lookup_desc.a + v14[2];
        result[i][3] = lookup_desc.a + v14[3];
      }
      break;
    }
    case 1: {
      if (lookup_desc.b < limit) {
        std::uint8_t *v21 = (std::uint8_t *)&float_data[2 * lookup_desc.b] + ((four_times_sub_y + 1) >> 1);
        result[i][0] = lookup_desc.a + (v21[0] & 0xF);
        result[i][1] = lookup_desc.a + (v21[1] >> 4);
        result[i][2] = lookup_desc.a + (v21[1] & 0xF);
      } else {
        std::uint8_t *v19 = (std::uint8_t *)float_data_negative_ptr + four_times_sub_y + 16 * lookup_desc.b + 1;
        result[i][0] = lookup_desc.a + v19[0];
        result[i][1] = lookup_desc.a + v19[1];
        result[i][2] = lookup_desc.a + v19[2];
      }
      if (lookup_desc_1.b < limit)
        result[i][3] = lookup_desc_1.a + (*((std::uint8_t *)&float_data[2 * lookup_desc_1.b] + (four_times_sub_y >> 1)) >> 4);
      else
        result[i][3] = lookup_desc_1.a + *((std::uint8_t *)&float_data_negative_ptr[4 * lookup_desc_1.b] + four_times_sub_y);
      break;
    }
    case 2: {
      if (lookup_desc.b < limit) {
        std::uint8_t *v25 = (std::uint8_t *)&float_data[2 * lookup_desc.b] + ((four_times_sub_y + 2) >> 1);
        result[i][0] = lookup_desc.a + (v25[0] >> 4);
        result[i][1] = lookup_desc.a + (v25[0] & 0xF);
      } else {
        std::uint32_t v24 = four_times_sub_y + 16 * lookup_desc.b;
        result[i][0] = lookup_desc.a + *((std::uint8_t *)float_data_negative_ptr + v24 + 2);
        result[i][1] = lookup_desc.a + *((std::uint8_t *)float_data_negative_ptr + v24 + 3);
      }
      if (lookup_desc_1.b < limit) {
        std::uint8_t *v29 = (std::uint8_t *)&float_data[2 * lookup_desc_1.b] + (four_times_sub_y >> 1);
        result[i][2] = lookup_desc_1.a + (v29[0] >> 4);
        result[i][3] = lookup_desc_1.a + (v29[0] & 0xFu);
      } else {
        std::uint32_t v28 = four_times_sub_y + 16 * lookup_desc_1.b;
        result[i][2] = lookup_desc_1.a + *((std::uint8_t *)float_data_negative_ptr + v28);
        result[i][3] = lookup_desc_1.a + *((std::uint8_t *)float_data_negative_ptr + v28 + 1);
      }
      break;
    }
    case 3: {
      if (lookup_desc.b < limit)
        result[i][0] = lookup_desc.a + (*((std::uint8_t *)&float_data[2 * lookup_desc.b] + ((four_times_sub_y + 3) >> 1)) & 0xF);
      else
        result[i][0] = lookup_desc.a + *((std::uint8_t *)&float_data_negative_ptr[4 * lookup_desc.b] + four_times_sub_y + 3);
      if (lookup_desc_1.b < limit) {
        std::uint8_t *v35 = (std::uint8_t *)&float_data[2 * lookup_desc_1.b] + (four_times_sub_y >> 1);
        result[i][1] = lookup_desc_1.a + (v35[0] >> 4);
        result[i][2] = lookup_desc_1.a + (v35[0] & 0xFu);
        result[i][3] = lookup_desc_1.a + (v35[1] >> 4);
      } else {
        std::uint8_t *v33 = (std::uint8_t *)float_data_negative_ptr + four_times_sub_y + 16 * lookup_desc_1.b;
        result[i][1] = lookup_desc_1.a + v33[0];
        result[i][2] = lookup_desc_1.a + v33[1];
        result[i][3] = lookup_desc_1.a + v33[2];
      }
      break;
    }
    default:
      break;
    }
    four_times_sub_y += 4;
    if ((four_times_sub_y & 0xF0) != 0) {
      four_times_sub_y &= 0xFu;
      lookup_1 += num;
    }
  }
}

int main() {
  CLI::App app{"FUEL heightmap analyzer"};

  std::string binary_filename = "";
  std::string image_filename = "";
  app.add_option("-b,--binary", binary_filename, "Input binary file path")
      ->required();
  app.add_option("-i,--image", image_filename, "Output image path")->required();

  CLI11_PARSE(app);

  std::ifstream binary_file(binary_filename, std::ios::binary | std::ios::ate);
  if (!binary_file.good()) {
    std::cerr << "Failed to open binary file!\n";
    return 1;
  }
  std::streamsize binary_size = binary_file.tellg();
  binary_file.seekg(0, std::ios::beg);

  std::vector<std::uint8_t> binary_buffer(binary_size);

  if (!binary_file.read((char *)binary_buffer.data(), binary_size)) {
    std::cerr << "Failed to read binary file!\n";
    return 1;
  }

  std::uint32_t width = *(std::uint32_t *)(binary_buffer.data() + 0x20);
  std::uint32_t num = width / 4;
  std::uint32_t limit = *(std::uint32_t *)(binary_buffer.data() + 0x34);
  std::uint32_t float_data_size = *(std::uint32_t *)(binary_buffer.data() + 0x38);
  std::uint32_t *float_data = (std::uint32_t *)(binary_buffer.data() + 0x3C);
  LookupDescription *lookup = (LookupDescription*)(float_data + float_data_size - 1);

  float max = 1892;
  float min = 8;

  CImg<float> image(width, width, 1, 3, 0);

  float result[4][4];

  for (std::uint32_t x = 0; x < width - 3; ++x) {
    for (std::uint32_t y = 0; y < width - 3; ++y) {
      lookup_float(x, y, num, limit, float_data, lookup, result);
      std::uint32_t i_max = 1;
      std::uint32_t j_max = 1;
      if (x == width - 4) {
        i_max = 4;
      }
      if (y == width - 4) {
        j_max = 4;
      }
      for (std::uint32_t i = 0; i < i_max; ++i) {
        for (std::uint32_t j = 0; j < j_max; ++j) {
          for (std::uint32_t k = 0; k < 3; ++k) {
            image(x + i, y + j, k) = result[i][j];
          }
        }
      }
    }
  }

  image.normalize(0, 255);
  image.save_bmp(image_filename.c_str());

  return 0;
}
