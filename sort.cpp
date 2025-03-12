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
    // cout<<"�鲢����"<<endl;
    // for(int i=p;i<=r;i++){
    //         cout << A[i] << " ";
    // }
}
void MERGE_SORT(vector<int> &arr, int p, int r)
{
    // cout<<"��ǰ���й鲢���������"<<endl;
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
    // ����ѡȡ��һ������Ϊpivot
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
{ // i��ǰ�ڵ㣬n ����ģ
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
{ // Ͱ�ڲ�������
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
        cout << name << "������ɣ���ʱ" << elapsed.count() << "ms" << endl;
    }
    else
    {
        cout << name << "����ʧ�ܣ�" << endl;
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
        cout << name << "������ɣ���ʱ" << elapsed.count() << "ms" << endl;
    }
    else
    {
        cout << name << "����ʧ�ܣ�" << endl;
    }
}
int main()
{ cout<<"(1) �������һ������n�����������飨Ԫ��ȡֵ��Χ��1~1000�������ò������򡢹鲢���򡢿������򡢶����򡢻�������Ͱ������㷨��������зǽ������򣬼�¼��ͬ�㷨������ʱ�䡣"<<endl;
    srand((unsigned)time(0));
    int n;
    cout << "���������ģ" << endl;
    cin >> n;
    vector<int> arr = randomNum(n);
    // displayFirst50(arr);
    sortAndMeasureTime("��������", insertSort, arr);
    // displayFirst50(arr);
    sortAndMeasureTime("�鲢����", mergeSort, arr);
    sortAndMeasureTime("��������", quickSort, arr);
    sortAndMeasureTime("������", heapSort, arr);
    sortAndMeasureTime("��������", radixSort, arr);
    sortAndMeasureTime("Ͱ����", bucketSort, arr);
    cout<<"(2) �ı������ģn= 5��10��20��30��50�򣬼�¼��ͬ��ģ�¸����㷨������ʱ�䡣"<<endl;
    arr.clear();
    arr = randomNum(50000);
    cout << "5��" << endl;
    sortAndMeasureTime("��������", insertSort, arr);
    sortAndMeasureTime("�鲢����", mergeSort, arr);
    sortAndMeasureTime("��������", quickSort, arr);
    sortAndMeasureTime("������", heapSort, arr);
    sortAndMeasureTime("��������", radixSort, arr);
    sortAndMeasureTime("Ͱ����", bucketSort, arr);
    arr.clear();
    arr = randomNum(100000);
    cout << "10��" << endl;
    sortAndMeasureTime("��������", insertSort, arr);
    sortAndMeasureTime("�鲢����", mergeSort, arr);
    sortAndMeasureTime("��������", quickSort, arr);
    sortAndMeasureTime("������", heapSort, arr);
    sortAndMeasureTime("��������", radixSort, arr);
    sortAndMeasureTime("Ͱ����", bucketSort, arr);
    arr.clear();
    arr = randomNum(200000);
    cout << "20��" << endl;
    sortAndMeasureTime("��������", insertSort, arr);
    sortAndMeasureTime("�鲢����", mergeSort, arr);
    sortAndMeasureTime("��������", quickSort, arr);
    sortAndMeasureTime("������", heapSort, arr);
    sortAndMeasureTime("��������", radixSort, arr);
    sortAndMeasureTime("Ͱ����", bucketSort, arr);
    arr.clear();
    arr = randomNum(300000);
    cout << "30��" << endl;
    sortAndMeasureTime("��������", insertSort, arr);
    sortAndMeasureTime("�鲢����", mergeSort, arr);
    sortAndMeasureTime("��������", quickSort, arr);
    sortAndMeasureTime("������", heapSort, arr);
    sortAndMeasureTime("��������", radixSort, arr);
    sortAndMeasureTime("Ͱ����", bucketSort, arr);
    arr.clear();
    arr = randomNum(500000);
    cout << "50��" << endl;
    sortAndMeasureTime("��������", insertSort, arr);
    sortAndMeasureTime("�鲢����", mergeSort, arr);
    sortAndMeasureTime("��������", quickSort, arr);
    sortAndMeasureTime("������", heapSort, arr);
    sortAndMeasureTime("��������", radixSort, arr);
    sortAndMeasureTime("Ͱ����", bucketSort, arr);
    cout<<"(3) �Թ̶���ģ ��n = 10�򣩵��������������ң������Һ������������򲢼�¼�����㷨������ʱ�䡣��ʵ��Ҫ���ظ�5�Σ��۲��������ݷֲ�������ʱ��Ĺ�ϵ��"<<endl;
    arr.clear();
    n = 100000;
    arr = randomNum(n);
    for (int i = 0; i < 5; i++)
    {
        cout << "�������" << i+1 << endl;
        random_shuffle(arr.begin(), arr.end());
        sortAndMeasureTime1("��������", insertSort, arr);
        sortAndMeasureTime1("�鲢����", mergeSort, arr);
        sortAndMeasureTime1("��������", quickSort, arr);
        sortAndMeasureTime1("������", heapSort, arr);
        sortAndMeasureTime1("��������", radixSort, arr);
        sortAndMeasureTime1("Ͱ����", bucketSort, arr);
    }
    system("pause");
    return 0;
}
