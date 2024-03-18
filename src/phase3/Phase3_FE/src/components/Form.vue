<template>
    <el-row v-loading="loading">
        <el-col :span="22" :offset="1" :lg="{ span: 16, offset: 4 }">
            <el-card>
                <template #header>
                    <div class="card-header">
                        <span>Perth House Price Prediction</span>
                    </div>
                </template>
                <!-- form starts -->
                <el-form :model="form" ref="formRef" label-position="top" :rules="rules">
                    <el-row>
                        <el-col :span="11" :style="{ width: '100%' }">
                            <!-- bedroom field -->
                            <el-form-item label="Bedrooms" prop="bedrooms">
                                <el-select v-model="form.bedrooms" placeholder="Please select the bedrooms" clearable>
                                    <el-option v-for="bed in optionValues.bedrooms" :label="bed.label"
                                        :value="bed.value"></el-option>
                                </el-select>
                            </el-form-item>
                        </el-col>
                        <el-col :span="11" :offset="2">
                            <!-- bathroom field -->
                            <el-form-item label="Bathrooms" prop="bathrooms">
                                <el-select v-model="form.bathrooms" placeholder="Please select the bathrooms" clearable>
                                    <el-option v-for="bath in optionValues.bathrooms" :label="bath.label"
                                        :value="bath.value"></el-option>
                                </el-select>
                            </el-form-item>
                        </el-col>
                    </el-row>

                    <el-row>
                        <el-col :span="11">
                            <!-- garage field -->
                            <el-form-item label="Garages" prop="garages">
                                <el-select v-model="form.garages" placeholder="Please select the garages" clearable>
                                    <el-option v-for="grg in optionValues.garages" :label="grg.label"
                                        :value="grg.value"></el-option>
                                </el-select>
                            </el-form-item>
                        </el-col>
                    </el-row>


                    <!-- land area field -->
                    <el-form-item label="Land Area (sq mt)" prop="landArea">
                        <el-input type="number" v-model.number="form.landArea" placeholder="Please enter land area" />
                    </el-form-item>

                    <!-- floor area field -->
                    <el-form-item label="Floor Area (sq mt)" prop="floorArea">
                        <el-input type="number" v-model.number="form.floorArea" placeholder="Please enter floor area" />
                    </el-form-item>

                    <el-row>
                        <el-col :span="11" :style="{ width: '100%' }">
                            <!-- postal code field -->
                            <el-form-item label="Postal code" prop="postCode">
                                <el-select v-model="form.postCode" placeholder="Please select the postal code" filterable
                                    clearable>
                                    <el-option v-for="pc in optionValues.postCodes" :label="pc.label"
                                        :value="pc.value"></el-option>
                                </el-select>
                            </el-form-item>
                        </el-col>
                    </el-row>

                    <div class="action_btns">
                        <el-button type="primary" @click="onSubmit(formRef)">Get Prediction!</el-button>
                        <el-button @click="onClear(formRef)">Clear</el-button>
                    </div>
                </el-form>
            </el-card>
        </el-col>
    </el-row>
    <!-- dialog for price prediction -->
    <el-dialog v-model="predictionDialogVisible" :show-close="false">
        <el-result icon="success" title="Price Predicted!!">
            <template #extra>

                <el-descriptions title="Based on your inputs" direction="horizontal" :column="1" border>
                    <el-descriptions-item label="Price (AUD)">{{ prediction.price }}</el-descriptions-item>
                    <el-descriptions-item label="Category">{{ prediction.category }} <el-popover placement="top-start"
                            title="Price Ranges" :width="200" trigger="hover">
                            <div class="price-range">
                                <span>&lt; 415000 : LOW</span>
                                <span>(415000 - 755000) : MEDIUM</span>
                                <span>&gt; 755000 : HIGH</span>
                            </div>
                            <template #reference>
                                <svg style="cursor: pointer;" height="12px" width="20px" xmlns="http://www.w3.org/2000/svg"
                                    viewBox="0 0 1024 1024" data-v-ea893728="">
                                    <path fill="currentColor"
                                        d="M512 64a448 448 0 1 1 0 896.064A448 448 0 0 1 512 64m67.2 275.072c33.28 0 60.288-23.104 60.288-57.344s-27.072-57.344-60.288-57.344c-33.28 0-60.16 23.104-60.16 57.344s26.88 57.344 60.16 57.344M590.912 699.2c0-6.848 2.368-24.64 1.024-34.752l-52.608 60.544c-10.88 11.456-24.512 19.392-30.912 17.28a12.992 12.992 0 0 1-8.256-14.72l87.68-276.992c7.168-35.136-12.544-67.2-54.336-71.296-44.096 0-108.992 44.736-148.48 101.504 0 6.784-1.28 23.68.064 33.792l52.544-60.608c10.88-11.328 23.552-19.328 29.952-17.152a12.8 12.8 0 0 1 7.808 16.128L388.48 728.576c-10.048 32.256 8.96 63.872 55.04 71.04 67.84 0 107.904-43.648 147.456-100.416z">
                                    </path>
                                </svg>
                            </template>
                        </el-popover>
                    </el-descriptions-item>
                </el-descriptions>
                <br>
                <el-descriptions title="Approximate Distances to nearest (in metres)" direction="horizontal" :column="1"
                    border>
                    <el-descriptions-item label="Central Business District">{{ prediction.cbdDistance
                    }}</el-descriptions-item>
                    <el-descriptions-item label="Station">{{ prediction.nearestStationDistance }}</el-descriptions-item>
                    <el-descriptions-item label="High School">{{ prediction.nearestSchoolDistance }}</el-descriptions-item>
                </el-descriptions>
                <br>
                <el-link type="primary" @click="graphDialogVisible = true; predictionDialogVisible = false">More about our
                    model?</el-link>
                <br><br>
                <el-button type="primary" @click="closeDialog">Close</el-button>
            </template>
        </el-result>
    </el-dialog>
    <!-- dialog for graphs -->
    <el-dialog v-model="graphDialogVisible" :show-close="false">
        <el-carousel indicator-position="outside" :autoplay="false" height="550px">
            <el-carousel-item v-for="item in graphs" :key="item.img">
                <div class="center">
                    <img :src="item.img" class="graph_img">
                    <br><br>
                    <div>
                        {{ item.desc }}
                    </div>
                </div>
            </el-carousel-item>
        </el-carousel>
        <div class="center">
            <el-button type="primary" @click="graphDialogVisible = false; predictionDialogVisible = true">Close</el-button>
        </div>
    </el-dialog>
</template>

<script setup>
import { reactive, ref } from 'vue'
import axios from "axios"
import { ElMessage } from 'element-plus';
import residual from "../assets/residual.png";
import importance from "../assets/importance.png";

// form fields
const form = ref({
    "bedrooms": undefined,
    "bathrooms": undefined,
    "garages": undefined,
    "landArea": undefined,
    "floorArea": undefined,
    "postCode": undefined
})

// booleans for dialog visibility
const predictionDialogVisible = ref(false)
const graphDialogVisible = ref(false)

// used for storing results
const prediction = ref({
    price: 0,
    category: "",
    cbdDistance: 0,
    nearestStationDistance: 0,
    nearestSchoolDistance: 0
})
const loading = ref(false)
const graphs = ref([
    {
        img: residual,
        desc: "This chart is a histogram showing the spread of residual values, which represent the variance between the actual observed data and the predictions made by our model on testing data which was used to evaluate our model. In essence, since a large number of the residuals are close to zero, it implies that the discrepancy between what our model predicts and the actual results is minimal, suggesting a lower likelihood of error in the model's predictions.",
    },
    {
        img: importance,
        desc: "The chart illustrates how various factors weigh on our model's ability to forecast housing prices. It indicates that the pricing is greatly influenced by the postcode and the floor area, while the number of bathrooms and the presence of a garage have the somewhat influence.",
    }
])

const nonNegativeValidator = (rule, value, callback) => {
    if (value > 0) {
        callback()
    } else {
        callback("Please enter value greater than 0")
    }
}

// rules for form inputs
const rules = ref({
    bedrooms: [{ required: true, message: "Please select the bedrooms", trigger: ['change', 'blur'] }],
    bathrooms: [{ required: true, message: "Please select the bathrooms", trigger: ['change', 'blur'] }],
    garages: [{ required: true, message: "Please select the garages", trigger: ['change', 'blur'] }],
    landArea: [{ required: true, validator: nonNegativeValidator, trigger: 'change' }],
    floorArea: [{ required: true, validator: nonNegativeValidator, trigger: 'change' }],
    postCode: [{ required: true, message: "Please select the post code", trigger: ['change', 'blur'] }]
})
const formRef = ref()

// dropdown values for forms
const optionValues = reactive({
    bedrooms: [
        { value: 1, label: "1" },
        { value: 2, label: "2" },
        { value: 3, label: "3" },
        { value: 4, label: "4" },
        { value: 5, label: "5" },
        { value: 6, label: "6" },
        { value: 7, label: "7" }
    ],
    bathrooms: [
        { value: 1, label: "1" },
        { value: 2, label: "2" },
        { value: 3, label: "3" },
        { value: 4, label: "4" },
    ],
    garages: [
        { value: 1, label: "1" },
        { value: 2, label: "2" },
        { value: 3, label: "3" },
        { value: 4, label: "4" },
        { value: 5, label: "5" },
        { value: 6, label: "6" },
        { value: 7, label: "7" },
        { value: 8, label: "8" }
    ],
    postCodes: [
        {
            "value": 6056,
            "label": "6056"
        },
        {
            "value": 6065,
            "label": "6065"
        },
        {
            "value": 6112,
            "label": "6112"
        },
        {
            "value": 6164,
            "label": "6164"
        },
        {
            "value": 6030,
            "label": "6030"
        },
        {
            "value": 6167,
            "label": "6167"
        },
        {
            "value": 6027,
            "label": "6027"
        },
        {
            "value": 6055,
            "label": "6055"
        },
        {
            "value": 6163,
            "label": "6163"
        },
        {
            "value": 6107,
            "label": "6107"
        },
        {
            "value": 6018,
            "label": "6018"
        },
        {
            "value": 6054,
            "label": "6054"
        },
        {
            "value": 6028,
            "label": "6028"
        },
        {
            "value": 6152,
            "label": "6152"
        },
        {
            "value": 6069,
            "label": "6069"
        },
        {
            "value": 6020,
            "label": "6020"
        },
        {
            "value": 6111,
            "label": "6111"
        },
        {
            "value": 6169,
            "label": "6169"
        },
        {
            "value": 6110,
            "label": "6110"
        },
        {
            "value": 6025,
            "label": "6025"
        },
        {
            "value": 6064,
            "label": "6064"
        },
        {
            "value": 6076,
            "label": "6076"
        },
        {
            "value": 6153,
            "label": "6153"
        },
        {
            "value": 6168,
            "label": "6168"
        },
        {
            "value": 6148,
            "label": "6148"
        },
        {
            "value": 6147,
            "label": "6147"
        },
        {
            "value": 6050,
            "label": "6050"
        },
        {
            "value": 6057,
            "label": "6057"
        },
        {
            "value": 6031,
            "label": "6031"
        },
        {
            "value": 6104,
            "label": "6104"
        },
        {
            "value": 6036,
            "label": "6036"
        },
        {
            "value": 6150,
            "label": "6150"
        },
        {
            "value": 6156,
            "label": "6156"
        },
        {
            "value": 6154,
            "label": "6154"
        },
        {
            "value": 6061,
            "label": "6061"
        },
        {
            "value": 6063,
            "label": "6063"
        },
        {
            "value": 6010,
            "label": "6010"
        },
        {
            "value": 6062,
            "label": "6062"
        },
        {
            "value": 6162,
            "label": "6162"
        },
        {
            "value": 6014,
            "label": "6014"
        },
        {
            "value": 6024,
            "label": "6024"
        },
        {
            "value": 6081,
            "label": "6081"
        },
        {
            "value": 6008,
            "label": "6008"
        },
        {
            "value": 6122,
            "label": "6122"
        },
        {
            "value": 6021,
            "label": "6021"
        },
        {
            "value": 6155,
            "label": "6155"
        },
        {
            "value": 6052,
            "label": "6052"
        },
        {
            "value": 6071,
            "label": "6071"
        },
        {
            "value": 6149,
            "label": "6149"
        },
        {
            "value": 6151,
            "label": "6151"
        },
        {
            "value": 6060,
            "label": "6060"
        },
        {
            "value": 6173,
            "label": "6173"
        },
        {
            "value": 6026,
            "label": "6026"
        },
        {
            "value": 6019,
            "label": "6019"
        },
        {
            "value": 6157,
            "label": "6157"
        },
        {
            "value": 6172,
            "label": "6172"
        },
        {
            "value": 6101,
            "label": "6101"
        },
        {
            "value": 6170,
            "label": "6170"
        },
        {
            "value": 6175,
            "label": "6175"
        },
        {
            "value": 6100,
            "label": "6100"
        },
        {
            "value": 6102,
            "label": "6102"
        },
        {
            "value": 6105,
            "label": "6105"
        },
        {
            "value": 6082,
            "label": "6082"
        },
        {
            "value": 6009,
            "label": "6009"
        },
        {
            "value": 6166,
            "label": "6166"
        },
        {
            "value": 6016,
            "label": "6016"
        },
        {
            "value": 6066,
            "label": "6066"
        },
        {
            "value": 6070,
            "label": "6070"
        },
        {
            "value": 6015,
            "label": "6015"
        },
        {
            "value": 6123,
            "label": "6123"
        },
        {
            "value": 6073,
            "label": "6073"
        },
        {
            "value": 6058,
            "label": "6058"
        },
        {
            "value": 6109,
            "label": "6109"
        },
        {
            "value": 6124,
            "label": "6124"
        },
        {
            "value": 6022,
            "label": "6022"
        },
        {
            "value": 6072,
            "label": "6072"
        },
        {
            "value": 6074,
            "label": "6074"
        },
        {
            "value": 6029,
            "label": "6029"
        },
        {
            "value": 6038,
            "label": "6038"
        },
        {
            "value": 6108,
            "label": "6108"
        },
        {
            "value": 6035,
            "label": "6035"
        },
        {
            "value": 6158,
            "label": "6158"
        },
        {
            "value": 6556,
            "label": "6556"
        },
        {
            "value": 6023,
            "label": "6023"
        },
        {
            "value": 6077,
            "label": "6077"
        },
        {
            "value": 6012,
            "label": "6012"
        },
        {
            "value": 6171,
            "label": "6171"
        },
        {
            "value": 6053,
            "label": "6053"
        },
        {
            "value": 6007,
            "label": "6007"
        },
        {
            "value": 6125,
            "label": "6125"
        },
        {
            "value": 6011,
            "label": "6011"
        },
        {
            "value": 6034,
            "label": "6034"
        },
        {
            "value": 6174,
            "label": "6174"
        },
        {
            "value": 6121,
            "label": "6121"
        },
        {
            "value": 6078,
            "label": "6078"
        },
        {
            "value": 6037,
            "label": "6037"
        },
        {
            "value": 6176,
            "label": "6176"
        },
        {
            "value": 6051,
            "label": "6051"
        },
        {
            "value": 6059,
            "label": "6059"
        },
        {
            "value": 6006,
            "label": "6006"
        },
        {
            "value": 6159,
            "label": "6159"
        },
        {
            "value": 6103,
            "label": "6103"
        },
        {
            "value": 6083,
            "label": "6083"
        },
        {
            "value": 6160,
            "label": "6160"
        },
        {
            "value": 6003,
            "label": "6003"
        },
        {
            "value": 6017,
            "label": "6017"
        },
        {
            "value": 6005,
            "label": "6005"
        },
        {
            "value": 6004,
            "label": "6004"
        },
        {
            "value": 6033,
            "label": "6033"
        },
        {
            "value": 6558,
            "label": "6558"
        },
        {
            "value": 6165,
            "label": "6165"
        },
        {
            "value": 6106,
            "label": "6106"
        }
    ]
})

// action to be done on submit click
const onSubmit = (formEl) => {
    formEl.validate((valid) => {
        if (valid) {
            // if form is valid then call api
            fetchPrediction()
        } else {
            ElMessage.warning("Please enter the form fields")
        }
    })
}

// prediction api
const fetchPrediction = () => {
    loading.value = true
    axios.post('http://127.0.0.1:8000/predict', {
        ...form.value
    })
        .then(res => {
            // populate result
            prediction.value = res.data
            loading.value = false
            predictionDialogVisible.value = true
        }).catch(err => {
            loading.value = false
            ElMessage.error('An error occurred!')
        })
}

const closeDialog = () => {
    predictionDialogVisible.value = false
    prediction.value = {
        price: 0,
        category: "",
        cbdDistance: 0,
        nearestStationDistance: 0,
        nearestSchoolDistance: 0
    }
}

const onClear = () => {
    form.value = {
        bedrooms: undefined,
        bathrooms: undefined,
        garages: undefined,
        landArea: undefined,
        floorArea: undefined,
        postCodes: undefined
    }
}
</script>
  