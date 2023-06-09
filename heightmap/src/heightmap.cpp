#include <CImg.h>
#include <CLI/CLI.hpp>
#include <algorithm>
#include <atomic>
#include <cstdint>
#include <exception>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <string>
#include <vector>

using namespace cimg_library;

struct LookupDescription {
  std::uint32_t horizon : 12;
  std::uint32_t altitudes_index : 20;
};

struct AltitudePack {
  std::uint8_t odd : 4;
  std::uint8_t even : 4;
};

/// This function is a cleaned up decompilation of the original function in the
/// game
void lookup_4x4_floats(std::uint32_t x, std::uint32_t y, std::uint32_t num,
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
      if (lookup_desc.altitudes_index < limit) {
        std::uint8_t *v17 =
            (std::uint8_t *)&float_data[2 * lookup_desc.altitudes_index] +
            (four_times_sub_y >> 1);
        result[i][0] = lookup_desc.horizon + (v17[0] >> 4);
        result[i][1] = lookup_desc.horizon + (v17[0] & 0xF);
        result[i][2] = lookup_desc.horizon + (v17[1] >> 4);
        result[i][3] = lookup_desc.horizon + (v17[1] & 0xFu);
      } else {
        std::uint8_t *v14 = (std::uint8_t *)float_data_negative_ptr +
                            four_times_sub_y + 16 * lookup_desc.altitudes_index;
        result[i][0] = lookup_desc.horizon + v14[0];
        result[i][1] = lookup_desc.horizon + v14[1];
        result[i][2] = lookup_desc.horizon + v14[2];
        result[i][3] = lookup_desc.horizon + v14[3];
      }
      break;
    }
    case 1: {
      if (lookup_desc.altitudes_index < limit) {
        std::uint8_t *v21 =
            (std::uint8_t *)&float_data[2 * lookup_desc.altitudes_index] +
            ((four_times_sub_y + 1) >> 1);
        result[i][0] = lookup_desc.horizon + (v21[0] & 0xF);
        result[i][1] = lookup_desc.horizon + (v21[1] >> 4);
        result[i][2] = lookup_desc.horizon + (v21[1] & 0xF);
      } else {
        std::uint8_t *v19 = (std::uint8_t *)float_data_negative_ptr +
                            four_times_sub_y +
                            16 * lookup_desc.altitudes_index + 1;
        result[i][0] = lookup_desc.horizon + v19[0];
        result[i][1] = lookup_desc.horizon + v19[1];
        result[i][2] = lookup_desc.horizon + v19[2];
      }
      if (lookup_desc_1.altitudes_index < limit)
        result[i][3] =
            lookup_desc_1.horizon +
            (*((std::uint8_t *)&float_data[2 * lookup_desc_1.altitudes_index] +
               (four_times_sub_y >> 1)) >>
             4);
      else
        result[i][3] =
            lookup_desc_1.horizon + *((std::uint8_t *)&float_data_negative_ptr
                                          [4 * lookup_desc_1.altitudes_index] +
                                      four_times_sub_y);
      break;
    }
    case 2: {
      if (lookup_desc.altitudes_index < limit) {
        std::uint8_t *v25 =
            (std::uint8_t *)&float_data[2 * lookup_desc.altitudes_index] +
            ((four_times_sub_y + 2) >> 1);
        result[i][0] = lookup_desc.horizon + (v25[0] >> 4);
        result[i][1] = lookup_desc.horizon + (v25[0] & 0xF);
      } else {
        std::uint32_t v24 = four_times_sub_y + 16 * lookup_desc.altitudes_index;
        result[i][0] = lookup_desc.horizon +
                       *((std::uint8_t *)float_data_negative_ptr + v24 + 2);
        result[i][1] = lookup_desc.horizon +
                       *((std::uint8_t *)float_data_negative_ptr + v24 + 3);
      }
      if (lookup_desc_1.altitudes_index < limit) {
        std::uint8_t *v29 =
            (std::uint8_t *)&float_data[2 * lookup_desc_1.altitudes_index] +
            (four_times_sub_y >> 1);
        result[i][2] = lookup_desc_1.horizon + (v29[0] >> 4);
        result[i][3] = lookup_desc_1.horizon + (v29[0] & 0xFu);
      } else {
        std::uint32_t v28 =
            four_times_sub_y + 16 * lookup_desc_1.altitudes_index;
        result[i][2] = lookup_desc_1.horizon +
                       *((std::uint8_t *)float_data_negative_ptr + v28);
        result[i][3] = lookup_desc_1.horizon +
                       *((std::uint8_t *)float_data_negative_ptr + v28 + 1);
      }
      break;
    }
    case 3: {
      if (lookup_desc.altitudes_index < limit)
        result[i][0] =
            lookup_desc.horizon +
            (*((std::uint8_t *)&float_data[2 * lookup_desc.altitudes_index] +
               ((four_times_sub_y + 3) >> 1)) &
             0xF);
      else
        result[i][0] =
            lookup_desc.horizon +
            *((std::uint8_t
                   *)&float_data_negative_ptr[4 * lookup_desc.altitudes_index] +
              four_times_sub_y + 3);
      if (lookup_desc_1.altitudes_index < limit) {
        std::uint8_t *v35 =
            (std::uint8_t *)&float_data[2 * lookup_desc_1.altitudes_index] +
            (four_times_sub_y >> 1);
        result[i][1] = lookup_desc_1.horizon + (v35[0] >> 4);
        result[i][2] = lookup_desc_1.horizon + (v35[0] & 0xFu);
        result[i][3] = lookup_desc_1.horizon + (v35[1] >> 4);
      } else {
        std::uint8_t *v33 = (std::uint8_t *)float_data_negative_ptr +
                            four_times_sub_y +
                            16 * lookup_desc_1.altitudes_index;
        result[i][1] = lookup_desc_1.horizon + v33[0];
        result[i][2] = lookup_desc_1.horizon + v33[1];
        result[i][3] = lookup_desc_1.horizon + v33[2];
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

class HeightMap {
public:
  HeightMap(std::string binary_filename) {
    std::ifstream binary_file(binary_filename,
                              std::ios::binary | std::ios::ate);
    if (!binary_file.good()) {
      std::cerr << "Failed to open binary file!\n";
      throw 1;
    }
    std::streamsize binary_size = binary_file.tellg();
    binary_file.seekg(0, std::ios::beg);

    m_binary_buffer.resize(binary_size);

    if (!binary_file.read((char *)m_binary_buffer.data(), binary_size)) {
      std::cerr << "Failed to read binary file!\n";
      throw 1;
    }

    m_width = *(std::uint32_t *)(m_binary_buffer.data() + 0x20);
    m_lookup_width = m_width / 4;
    m_packed_altitudes_size = *(std::uint32_t *)(m_binary_buffer.data() + 0x34);
    m_float_data_size = *(std::uint32_t *)(m_binary_buffer.data() + 0x38);
    m_float_data = (std::uint32_t *)(m_binary_buffer.data() + 0x3C);
    m_lookup = (LookupDescription *)(m_float_data + m_float_data_size - 1);
    m_altitudes_packed = reinterpret_cast<AltitudePack(*)[8]>(m_float_data);
    m_altitudes_unpacked = reinterpret_cast<std::uint8_t(*)[16]>(
        m_altitudes_packed + m_packed_altitudes_size);
  }

  /// This function is based on lookup_4x4_floats and looks up the value at a
  /// single point
  std::uint32_t at(std::uint32_t x, std::uint32_t y) {
    LookupDescription lookup_desc =
        m_lookup[(x / 4) + m_lookup_width * (y / 4)];
    std::uint32_t offset = (x % 4) + (4 * (y % 4));

    std::uint8_t altitude;
    if (lookup_desc.altitudes_index < m_packed_altitudes_size) {
      AltitudePack altitude_pack =
          m_altitudes_packed[lookup_desc.altitudes_index][offset / 2];
      altitude = x % 2 == 0 ? altitude_pack.even : altitude_pack.odd;
    } else {
      altitude = m_altitudes_unpacked[lookup_desc.altitudes_index -
                                      m_packed_altitudes_size][offset];
    }

    return lookup_desc.horizon + altitude;
  }

  CImg<std::uint32_t> to_image() {
    CImg<std::uint32_t> image(m_width, m_width, 1, 1, 0);

    for (std::uint32_t x = 0; x < m_width; ++x) {
      for (std::uint32_t y = 0; y < m_width; ++y) {
        image(x, y) = at(x, y);
      }
    }

    return image;
  }

private:
  std::vector<std::uint8_t> m_binary_buffer;
  std::uint32_t m_width;
  std::uint32_t m_lookup_width;
  std::uint32_t m_packed_altitudes_size;
  std::uint32_t m_float_data_size;
  std::uint32_t *m_float_data;
  LookupDescription *m_lookup;
  AltitudePack (*m_altitudes_packed)[8];
  std::uint8_t (*m_altitudes_unpacked)[16];
};

int main() {
  CLI::App app{"FUEL heightmap analyzer"};

  std::string binary_filename = "";
  std::string image_filename = "";
  app.add_option("-b,--binary", binary_filename, "Input binary file path")
      ->required();
  app.add_option("-i,--image", image_filename, "Output image path")->required();

  CLI11_PARSE(app);

  HeightMap height_map(binary_filename);

  CImg<std::uint32_t> image = height_map.to_image();

  image.normalize(0, 255);
  image.save_bmp(image_filename.c_str());

  return 0;
}
