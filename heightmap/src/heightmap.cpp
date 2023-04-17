#include <CImg.h>
#include <CLI/CLI.hpp>
#include <atomic>
#include <cstdint>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <string>
#include <vector>

using namespace cimg_library;

struct Result {
  float a;
  float b;
  float c;
  float d;
};

void lookup_float(std::uint32_t x, std::uint32_t y, std::uint32_t num,
                  std::uint32_t limit, std::uint32_t *float_data,
                  std::uint32_t *lookup, Result *result) {
  std::uint32_t *float_data_negative_ptr =
      float_data - limit * 2;

  std::uint32_t sub_x = x & 3;
  std::uint32_t *lookup_1 = &lookup[(x >> 2) + num * (y >> 2)];

  std::uint32_t four_times_sub_y = 4 * (y & 3);
  for (std::uint32_t i = 0; i < 4; ++i) {
    std::uint32_t lookup_desc = *(lookup_1 - 1);
    std::uint32_t v11 = lookup_desc & 0xFFF;
    std::uint32_t v12 = lookup_desc >> 12;
    switch (sub_x) {
    case 0: {
      if (v12 < limit) {
        std::uint8_t *v17 =
            (std::uint8_t *)&float_data[2 * v12] + (four_times_sub_y >> 1);
        result->a = (float)(v11 + ((std::uint8_t)*v17 >> 4));
        result->b = (float)(v11 + (*v17++ & 0xF));
        result->c = (float)(v11 + ((std::uint8_t)*v17 >> 4));
        result->d = (double)(v11 + (*v17 & 0xFu));
      } else {
        std::uint32_t v13 = four_times_sub_y + 16 * v12;
        std::int32_t v14 = *((std::uint8_t *)float_data_negative_ptr + v13);
        std::uint8_t *v15 = (std::uint8_t *)float_data_negative_ptr + v13 + 1;
        result->a = (float)(unsigned int)(v11 + v14);
        result->b = (float)(v11 + *v15++);
        result->c = (float)(v11 + (unsigned int)*v15);
        result->d = (double)(v11 + (unsigned int)v15[1]);
      }
      break;
    }
    case 1: {
      if (v12 < limit) {
        std::uint8_t *v21 = (std::uint8_t *)&float_data[2 * v12] +
                            ((four_times_sub_y + 1) >> 1);
        result->a = (float)(v11 + (*v21++ & 0xF));
        result->b = (float)(v11 + ((std::uint8_t)*v21 >> 4));
        result->c = (float)(v11 + (*v21 & 0xF));
      } else {
        std::uint32_t v18 = four_times_sub_y + 16 * v12;
        std::int32_t v19 = *((std::uint8_t *)float_data_negative_ptr + v18 + 1);
        std::uint8_t *v20 = (std::uint8_t *)float_data_negative_ptr + v18 + 2;
        result->a = (float)(unsigned int)(v11 + v19);
        result->b = (float)(v11 + (unsigned int)*v20);
        result->c = (float)(v11 + v20[1]);
      }
      std::uint32_t v22 = *lookup_1 >> 12;
      std::int32_t v23 = *lookup_1 & 0xFFF;
      if (v22 < limit)
        result->d = (double)(v23 + (*((std::uint8_t *)&float_data[2 * v22] +
                                      (four_times_sub_y >> 1)) >>
                                    4));
      else
        result->d =
            (double)(v23 +
                     (unsigned int)*(
                         (std::uint8_t *)&float_data_negative_ptr[4 * v22] +
                         four_times_sub_y));
      break;
    }
    case 2: {
      if (v12 < limit) {
        std::uint8_t *v25 = (std::uint8_t *)&float_data[2 * v12] +
                            ((four_times_sub_y + 2) >> 1);
        result->a = (float)(v11 + ((std::uint8_t)*v25 >> 4));
        result->b = (float)(v11 + (*v25 & 0xF));
      } else {
        std::uint32_t v24 = four_times_sub_y + 16 * v12;
        result->a = (float)(v11 + (unsigned int)*(
                                      (std::uint8_t *)float_data_negative_ptr +
                                      v24 + 2));
        result->b =
            (float)(v11 + *((std::uint8_t *)float_data_negative_ptr + v24 + 3));
      }
      std::uint32_t v26 = *lookup_1 >> 12;
      std::int32_t v27 = *lookup_1 & 0xFFF;
      if (v26 < limit) {
        std::uint8_t *v29 =
            (std::uint8_t *)&float_data[2 * v26] + (four_times_sub_y >> 1);
        result->c = (float)(v27 + ((std::uint8_t)*v29 >> 4));
        result->d = (double)(v27 + (*v29 & 0xFu));
      } else {
        std::uint32_t v28 = four_times_sub_y + 16 * v26;
        result->c =
            (float)(v27 + (unsigned int)*(
                              (std::uint8_t *)float_data_negative_ptr + v28));
        result->d = (double)(v27 + (unsigned int)*(
                                       (std::uint8_t *)float_data_negative_ptr +
                                       v28 + 1));
      }
      break;
    }
    case 3: {
      if (v12 < limit)
        result->a = (float)(v11 + (*((std::uint8_t *)&float_data[2 * v12] +
                                     ((four_times_sub_y + 3) >> 1)) &
                                   0xF));
      else
        result->a =
            (float)(v11 + *((std::uint8_t *)&float_data_negative_ptr[4 * v12] +
                            four_times_sub_y + 3));
      std::uint32_t v30 = *lookup_1 >> 12;
      std::int32_t v31 = *lookup_1 & 0xFFF;
      if (v30 < limit) {
        std::uint8_t *v35 =
            (std::uint8_t *)&float_data[2 * v30] + (four_times_sub_y >> 1);
        result->b = (float)(v31 + (*v35 >> 4));
        result->c = (float)(v31 + (*v35 & 0xFu));
        result->d = (double)(v31 + (v35[1] >> 4));
      } else {
        std::uint32_t v32 = four_times_sub_y + 16 * v30;
        std::int32_t v33 = *((std::uint8_t *)float_data_negative_ptr + v32);
        std::uint8_t *v34 = (std::uint8_t *)float_data_negative_ptr + v32 + 1;
        result->b = (float)(unsigned int)(v31 + v33);
        result->c = (float)(v31 + (unsigned int)*v34);
        result->d = (double)(v31 + (unsigned int)v34[1]);
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
    ++result;
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
  std::uint32_t float_data_size =
      *(std::uint32_t *)(binary_buffer.data() + 0x38);
  std::uint32_t *float_data = (std::uint32_t *)(binary_buffer.data() + 0x3C);
  std::uint32_t *lookup = float_data + float_data_size;

  //// CImg<unsigned char> image(width,width,1,3);

  Result result[4];

  for (std::uint32_t x = 0; x < width - 3; ++x) {
      for (std::uint32_t y = 0; y < width - 3; ++y) {
          lookup_float(x, y, num, limit, float_data, lookup, result);
          // image.atXY(x, y, 0, 0) = result[0].a;
          // image.atXY(x, y, 0, 1) = result[0].b;
          // image.atXY(x, y, 0, 2) = result[0].c;
      }
  }

  //// image.save(image_filename.c_str());

    std::cout << "SUCCESS\n";

  return 0;
}
