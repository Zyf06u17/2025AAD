#include <iostream>
#include <vector>
#include <cstdlib>
#include <ctime>
#include <chrono>
#include <string>
#include <algorithm>
#include <unordered_map>
#include <functional>
#include <random>
using namespace std;
bool isSorted(const vector<int> &arr)
{
    for (size_t i = 1; i < arr.size(); i++)
    {
        if (arr[i - 1] > arr[i])
        {
            return false;
        }
    }
    return true;
}
vector<int> randomNum(int n)
{
    vector<int> arr(n);

    for (int i = 0; i < n; i++)
    {
        arr[i] = rand() % 1000 + 1;
    }
    return arr;
}
void disArr(vector<int> arr)
{
    for (int i = 0; i < arr.size(); i++)
    {
        cout << arr[i] << " ";
    }
    cout << endl;
}
void displayFirst50(const vector<int> &arr)
{
    int count = min(50, static_cast<int>(arr.size()));
    for (int i = 0; i < count; i++)
    {
        cout << arr[i] << " ";
    }
    cout << endl;
}
void bubbleSort(vector<int> &arr)
{
    bool swapped;
    for (int i = 0; i < arr.size(); i++)
    {
        swapped = false;
        for (int j = 0; j < arr.size() - 1; j++)
        {
            if (arr[j] > arr[j + 1])
            {
                swap(arr[j], arr[j + 1]);
                swapped = true;
            }
        }
        if (!swapped)
            break;
    }
}
void insertSort(vector<int> &arr)
{
    int temp;
    for (int i = 1; i < arr.size(); i++)
    {
        temp = arr[i];
        int j = i - 1;
        while (j >= 0 && arr[j] > temp)
        {
            arr[j + 1] = arr[j];
            j--;
            /* code */
        }
        arr[j + 1] = temp;
    }
}
void MERGE(vector<int> &A, int p, int q, int r)
{
    int n1 = q - p + 1;
    int n2 = r - q;
    vector<int> L(n1 + 1);
    vector<int> R(n2 + 1);
    for (int i = 0; i < L.size() - 1; i++)
        L[i] = A[p + i];
    for (int j = 0; j < R.size() - 1; j++)
        R[j] = A[q + 1 + j];
    L[n1] = 1001;
    R[n2] = 1001;
    int i = 0, j = 0;
    for (int k = p; k <= r; k++)
    {
        if (L[i] < R[j])
        {
            A[k] = L[i];
            i++;
        }
        else
        {
            A[k] = R[j];
            j++;
        }
    }
    // cout<<"归并后结果"<<endl;
    // for(int i=p;i<=r;i++){
    //         cout << A[i] << " ";
    // }
}
void MERGE_SORT(vector<int> &arr, int p, int r)
{
    // cout<<"当前进行归并排序的数组"<<endl;
    // for (int i = p; i <= r; i++)
    // {
    //     cout << arr[i] << " ";
    // }
    // cout << endl;
    if (p < r)
    {
        int q = (p + r) / 2;
        MERGE_SORT(arr, p, q);
        MERGE_SORT(arr, q + 1, r);
        MERGE(arr, p, q, r);
    }
}
void mergeSort(vector<int> &arr)
{
    MERGE_SORT(arr, 0, arr.size() - 1);
}
int PARTITION(vector<int> &arr, int left, int right)
{
    // 这里选取第一个数作为pivot
    int pivot = arr[left];
    arr[left] = -1;
    int low = left, high = right;
    while (low < high)
    {
        if (arr[low] == -1)
        {
            if (arr[high] <= pivot)
            {
                swap(arr[low], arr[high]);
                low++;
            }
            else
            {
                high--;
            }
        }
        else
        {
            if (arr[low] >= pivot)
            {
                swap(arr[low], arr[high]);
                high--;
            }
            else
            {
                low++;
            }
        }
    }
    arr[low] = pivot;
    // cout<<"pivot ="<<pivot<<endl;
    // disArr(arr);
    return low;
}
void QUICKSORT(vector<int> &arr, int left, int right)
{
    if (left < right)
    {
        int partition_index = PARTITION(arr, left, right);
        QUICKSORT(arr, left, partition_index - 1);
        QUICKSORT(arr, partition_index + 1, right);
    }
}
void quickSort(vector<int> &arr)
{
    QUICKSORT(arr, 0, arr.size() - 1);
}
void heapify(vector<int> &arr, int n, int i)
{ // i当前节点，n 树规模
    int largest = i;
    int left = 2 * i + 1;
    int right = 2 * i + 2;
    if (left < n && arr[left] > arr[largest])
        largest = left;
    if (right < n && arr[right] > arr[largest])
        largest = right;
    if (largest != i)
    {
        swap(arr[i], arr[largest]);
        heapify(arr, n, largest);
    }
}
void heapSort(vector<int> &arr)
{
    int n = arr.size();
    for (int i = n / 2 - 1; i >= 0; i--)
        heapify(arr, n, i);
    for (int i = n - 1; i > 0; i--)
    {
        std::swap(arr[0], arr[i]);
        heapify(arr, i, 0);
    }
}
void radixSort(vector<int> &arr)
{
    int maxVal = *max_element(arr.begin(), arr.end());
    int exp = 1;
    while (maxVal / exp > 0)
    {
        vector<int> output(arr.size());
        int count[10] = {0};
        for (int i = 0; i < arr.size(); i++)
        {
            count[(arr[i] / exp) % 10]++;
        }
        for (int i = 1; i < 10; i++)
        {
            count[i] += count[i - 1];
        }
        for (int i = arr.size() - 1; i >= 0; i--)
        {
            output[count[(arr[i] / exp) % 10] - 1] = arr[i];
            count[(arr[i] / exp) % 10]--;
        }
        for (int i = 0; i < arr.size(); i++)
        {
            arr[i] = output[i];
        }
        exp *= 10;
    }
}
void bucketSort(vector<int> &arr)
{ // 桶内插入排序
    if (arr.empty())
        return;
    int minVal = 1;
    int maxVal = 1000;
    int bucketCount = 10;
    vector<vector<int>> buckets(bucketCount);
    int bucketRange = (maxVal - minVal) / bucketCount + 1;
    for (int num : arr)
    {
        int bucketIndex = (num - minVal) / bucketRange;
        buckets[bucketIndex].push_back(num);
    }
    for (auto &bucket : buckets)
    {
        quickSort(bucket);
    }
    int index = 0;
    for (const auto &bucket : buckets)
    {
        for (int num : bucket)
        {
            arr[index++] = num;
        }
    }
}
typedef void (*functionName)(vector<int> &);
void sortAndMeasureTime(const string name, functionName func, vector<int> arr)
{
    auto start = chrono::high_resolution_clock::now();
    func(arr);
    auto end = chrono::high_resolution_clock::now();
    chrono::duration<double, std::milli> elapsed = end - start;
    if (isSorted(arr))
    {
        cout << name << "排序完成，用时" << elapsed.count() << "ms" << endl;
    }
    else
    {
        cout << name << "排序失败！" << endl;
    }
}
void sortAndMeasureTime1(const string name, functionName func, vector<int> &arr)
{
    auto start = chrono::high_resolution_clock::now();
    func(arr);
    auto end = chrono::high_resolution_clock::now();
    chrono::duration<double, std::milli> elapsed = end - start;
    if (isSorted(arr))
    {
        cout << name << "排序完成，用时" << elapsed.count() << "ms" << endl;
    }
    else
    {
        cout << name << "排序失败！" << endl;
    }
}
int main()
{ cout<<"(1) 随机生成一个包括n个整数的数组（元素取值范围是1~1000），利用插入排序、归并排序、快速排序、堆排序、基数排序、桶排序等算法对数组进行非降序排序，记录不同算法的运行时间。"<<endl;
    srand((unsigned)time(0));
    int n;
    cout << "输入数组规模" << endl;
    cin >> n;
    vector<int> arr = randomNum(n);
    // displayFirst50(arr);
    sortAndMeasureTime("插入排序", insertSort, arr);
    // displayFirst50(arr);
    sortAndMeasureTime("归并排序", mergeSort, arr);
    sortAndMeasureTime("快速排序", quickSort, arr);
    sortAndMeasureTime("堆排序", heapSort, arr);
    sortAndMeasureTime("基数排序", radixSort, arr);
    sortAndMeasureTime("桶排序", bucketSort, arr);
    cout<<"(2) 改变数组规模n= 5万、10万、20万、30万、50万，记录不同规模下各个算法的排序时间。"<<endl;
    arr.clear();
    arr = randomNum(50000);
    cout << "5万：" << endl;
    sortAndMeasureTime("插入排序", insertSort, arr);
    sortAndMeasureTime("归并排序", mergeSort, arr);
    sortAndMeasureTime("快速排序", quickSort, arr);
    sortAndMeasureTime("堆排序", heapSort, arr);
    sortAndMeasureTime("基数排序", radixSort, arr);
    sortAndMeasureTime("桶排序", bucketSort, arr);
    arr.clear();
    arr = randomNum(100000);
    cout << "10万：" << endl;
    sortAndMeasureTime("插入排序", insertSort, arr);
    sortAndMeasureTime("归并排序", mergeSort, arr);
    sortAndMeasureTime("快速排序", quickSort, arr);
    sortAndMeasureTime("堆排序", heapSort, arr);
    sortAndMeasureTime("基数排序", radixSort, arr);
    sortAndMeasureTime("桶排序", bucketSort, arr);
    arr.clear();
    arr = randomNum(200000);
    cout << "20万：" << endl;
    sortAndMeasureTime("插入排序", insertSort, arr);
    sortAndMeasureTime("归并排序", mergeSort, arr);
    sortAndMeasureTime("快速排序", quickSort, arr);
    sortAndMeasureTime("堆排序", heapSort, arr);
    sortAndMeasureTime("基数排序", radixSort, arr);
    sortAndMeasureTime("桶排序", bucketSort, arr);
    arr.clear();
    arr = randomNum(300000);
    cout << "30万：" << endl;
    sortAndMeasureTime("插入排序", insertSort, arr);
    sortAndMeasureTime("归并排序", mergeSort, arr);
    sortAndMeasureTime("快速排序", quickSort, arr);
    sortAndMeasureTime("堆排序", heapSort, arr);
    sortAndMeasureTime("基数排序", radixSort, arr);
    sortAndMeasureTime("桶排序", bucketSort, arr);
    arr.clear();
    arr = randomNum(500000);
    cout << "50万：" << endl;
    sortAndMeasureTime("插入排序", insertSort, arr);
    sortAndMeasureTime("归并排序", mergeSort, arr);
    sortAndMeasureTime("快速排序", quickSort, arr);
    sortAndMeasureTime("堆排序", heapSort, arr);
    sortAndMeasureTime("基数排序", radixSort, arr);
    sortAndMeasureTime("桶排序", bucketSort, arr);
    cout<<"(3) 对固定规模 （n = 10万）的数组进行随机扰乱，对扰乱后的数组进行排序并记录各个算法的排序时间。本实验要求重复5次，观察输入数据分布和运行时间的关系。"<<endl;
    arr.clear();
    n = 100000;
    arr = randomNum(n);
    for (int i = 0; i < 5; i++)
    {
        cout << "随机扰乱" << i+1 << endl;
        random_shuffle(arr.begin(), arr.end());
        sortAndMeasureTime1("插入排序", insertSort, arr);
        sortAndMeasureTime1("归并排序", mergeSort, arr);
        sortAndMeasureTime1("快速排序", quickSort, arr);
        sortAndMeasureTime1("堆排序", heapSort, arr);
        sortAndMeasureTime1("基数排序", radixSort, arr);
        sortAndMeasureTime1("桶排序", bucketSort, arr);
    }
    system("pause");
    return 0;
}
